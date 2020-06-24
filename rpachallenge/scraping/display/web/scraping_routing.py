#!/usr/bin/python
#
# Copyright 2020 Walter Gildersleeve. All Rights Reserved.
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

from flask import render_template, Flask, request
from rpachallenge.scraping import ItemType

import math
from rpachallenge.scraping.display.web.link import Link

ScrapingWebsite = Flask(__name__)

def setDAO(dao):
    global _dao
    _dao = dao

@ScrapingWebsite.route('/')
def homePage():
    return render_template('index.html', vari="hello world!!")

@ScrapingWebsite.route('/list')
def displayItems():
    itemType = request.args.get('type', None)
    offset = int(request.args.get('offset', '0'))
    count = int(request.args.get('count', '10'))

    if not itemType:
        return render_template('items.html', links=buildLinks(None, offset, count), active="none")

    it = ItemType[itemType] if itemType != 'all' else None

    global _dao    
    items = _dao.getItems(offset, count, it) if itemType else None
    return render_template('items.html', items=items, links=buildLinks(it, offset, count), active=itemType if itemType else "all")

def buildLinks(itemType, offset, count):
    currentPage = math.trunc(offset / count) + 1
    if currentPage > 1:
        links = [ buildLink("<<<", itemType, 0, count), buildLink("<", itemType, offset - count, count) ]
    else:
        links = [ Link("<<<"), Link("<") ]

    total = _dao.getItemsCount(itemType)
    if total > count + offset:
        links.append(buildLink(">", itemType, offset + count, count))
        links.append(buildLink(">>>", itemType, total - count, count))
    else:
        links.append(Link(">>>"))
        links.append(Link(">"))

    return links

def buildLink(text, itemType, offset, count):
    url = "/list?offset={}&type={}&count={}".format(0 if offset < 0 else offset, itemType.name if itemType else "all", count)

    return Link(text, url)