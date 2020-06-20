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

"""Acts as the base object for capturing and presenting information on the page to be scraped.
"""

from rpachallenge.scraping.itemType import ItemType
from datetime import datetime

__author__ = 'walter.gildersleeve@uipath.com (Walter Gildersleeve)'

_NOWHEN = datetime(1970,1,1,0,0,0)

class Item:
    def __init__(self, itemType, url, title = None, description = None, creationDate = None, modificationDate = None):

        if not isinstance(itemType, ItemType):
            raise Exception("itemType must be one of ItemType")

        self._itemType = itemType

        if not isinstance(url, str) or not url.strip():
            raise Exception("The URL of the item must be provided")

        self._url = url.strip()

        if not title:
            title = self._url

        self._title = title

        if not description:
            description = self._title

        self._description = description

        if not creationDate:
            creationDate = modificationDate if modificationDate else _NOWHEN

        self._creationDate = creationDate

        if not modificationDate:
            modificationDate = self._creationDate
    
        self._modificationDate = modificationDate

    def getTitle(self):
        return self._title

    def getUrl(self):
        return self._url

    def getDescription(self):
        return self._description

    def getItemType(self):
        return self._itemType

    def getCreationDate(self):
        return self._creationDate

    def getModificationDate(self):
        return self._modificationDate

    def dateInvalid(self):
        return self.getModificationDate() == _NOWHEN

    def wasModified(self):
        return self.getCreationDate() != self.getModificationDate()