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

"""Base class for gathering new search items. Implementing classes must override the
stub method #getItems(itemType, maxNum)
"""

from rpachallenge.scraping import ItemType

__author__ = 'walter.gildersleeve@uipath.com (Walter Gildersleeve)'

class Engine:
    def __init__(self, searchTerms = "process automation"):
        self.searchTerms = searchTerms

    def getItems(self, itemType, maxNum = 100):
        """Generate and return items.

        Arguments:
        itemType: Item type to search for, as defined by the rpachallenge.scraping.ItemType enumeration
        maxNum: The maximum number of items to return; defaults to 100

        Returns:
        Returns a list of objects of type rpachallenge.scraping.Item. Number of items returned is between 
        0 and maxNum, inclusive.
        """
        raise Exception("Engine#getItems(itemType, maxNum) is undefined")

    def getSupportedTypes(self):
        """Indicates all the type supported by this engine, as indicated by the rpachallenge.scraping.ItemType enumeration.

        By default, all types are supported.
        """
        return list(ItemType)