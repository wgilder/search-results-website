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

from rpachallenge.scraping import ItemType
from rpachallenge.scraping import Item

class ItemsDao:
    """A very simple DAO in order to allow different implementations.
    """
    def __init__(self):
        pass

    def clear(self, itemType):
        raise NotImplementedError

    def clearAll(self):
        for itemType in ItemType:
            self.clear(itemType)

    def addItem(self, item):
        raise NotImplementedError

    def addItems(self, items):
        for item in items:
            self.addItem(item)

    def getItems(self, offset = 0, count = 100, itemType = None):
        raise NotImplementedError

    def destroy(self):
        pass # noop 

    def getItemsCount(self, itemType = None):
        raise NotImplementedError
