#!/usr/bin/python
#
# Copyright 2020 UiPath Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Concrete implementation of the Engine class, leveraging the Google Custom Search API
to get results from a subset of all websites. The attribute _CX is the CSE key being
used. It searches nearly 300 different domains for the desired information. The domains were
determined by publicly searching Google for "process automation" and using the returned domains.
The CSE can be seen at https://cse.google.com/cse?cx=003648246807547447764:vejoc3ypqqe

An App is also required for search. The attribute _KEY contains the key associated with
this.
"""

from googleapiclient.discovery import build
from rpachallenge.scraping import ItemType
from rpachallenge.scraping import Item
from dateutil.parser import parse
import re
import confuse
from datetime import datetime

import rpachallenge.scraping.populate.engine

# _CX='003648246807547447764:vejoc3ypqqe'
# _KEY='AIzaSyDEujTqUs6-sIDQCHxlITcT6U8oRlAFEZg'
_DATE_ATTRIBUTES = {
    ItemType.DOC.name + "-create": "creation date",
    ItemType.DOC.name + "-modify": "last saved date",
    ItemType.PDF.name + "-create": "creationdate",
    ItemType.PDF.name + "-modify": "moddate",
    ItemType.PPT.name + "-create": "creation date",
    ItemType.PPT.name + "-modify": "last saved date",
    ItemType.VIDEO.name + "-create": "datepublished",
    ItemType.VIDEO.name + "-modify": "datepublished"
}

# PDF files use ASN.1 date format, which isn't supported by dateutils.parser
_PDF_DATE=re.compile(r"^D:(\d{14}(?:[+-]\d{2})?)'?(Z|\d{2})'?$")

def _parseDate(rawDate):
    if not rawDate:
        return

    match = _PDF_DATE.match(rawDate)
    if match:
        rawDate = "%s%s" % (match[1], match[2])

    try:
        return parse(rawDate)
    except ValueError:
        return None 

class Engine(rpachallenge.scraping.populate.engine.Engine):
    def __init__(self):
        super().__init__()

        config = confuse.Configuration('RpaChallengeScraping')
        self.developerKey = config['google']['developerKey'].get()
        self.cseID = config['google']['cseID'].get()

    def _search(self, service, fileType, offset):
        if fileType == ItemType.VIDEO:
            return service.cse().list(q=self.searchTerms, cx=self.cseID, siteSearch='youtube.com', start=offset).execute()
        else:
            return service.cse().list(q=self.searchTerms, cx=self.cseID, fileType=fileType.value, start=offset).execute()

    def _getDates(self, item, itemType):
        if not 'pagemap' in item:
            return (None, None)

        if itemType == ItemType.VIDEO:
            if not 'videoobject' in item['pagemap']:
                return (None, None)
            obj = item['pagemap']['videoobject']
        elif not 'metatags' in item['pagemap']:
            return (None, None)
        else:
            obj = item['pagemap']['metatags']

        if not obj:
            return (None, None)

        obj = obj[0]
        cKey = _DATE_ATTRIBUTES[itemType.name + "-create"]
        mKey = _DATE_ATTRIBUTES[itemType.name + "-modify"]
        cDate = _parseDate(obj[cKey]) if cKey in obj else None
        mDate = _parseDate(obj[mKey]) if mKey in obj else None

        if cDate:
            if not mDate:
                mDate = cDate
        elif mDate:
            cDate = mDate


        return (cDate, mDate)

    def getItems(self, itemType, maxNum = 100):
        service = build("customsearch", "v1", developerKey=self.developerKey)
        results = list()
        offset = 1
        while len(results) < maxNum:
            res = self._search(service, itemType, offset)
            
            for idx in range(min(len(res['items']), maxNum - len(results))):
                item = res['items'][idx]
                url = item['link']
                title = item['title']
                description = item['snippet']
                (creationDate, modificationDate) = self._getDates(item, itemType)
                itemObject = Item(itemType, url, title, description, creationDate, modificationDate)
                results.append(itemObject)

            if res['queries'] and res['queries']['nextPage']:
                offset = res['queries']['nextPage'][0]['startIndex']
            else:
                break

        return results
