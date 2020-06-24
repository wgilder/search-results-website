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

import rpachallenge.scraping.dao.items
import mysql.connector
import threading
from rpachallenge.scraping import ItemType, Item

from rpachallenge.scraping import globals

_ADD_ITEM_SQL = "INSERT INTO items (url, type, title, description, creationDate, modificationDate) VALUES(%s,%s,%s,%s,%s,%s)"
_DELETE_ITEMS_BY_TYPE = "DELETE FROM items WHERE type=%s"
_DELETE_ALL_ITEMS = "DELETE FROM items"
_GET_ITEMS_SQL = "SELECT url,type,title,description,creationDate,modificationDate FROM items ORDER BY modificationDate DESC LIMIT %s OFFSET %s"
_GET_ITEMS_FILTERED_SQL = "SELECT url,type,title,description,creationDate,modificationDate FROM items WHERE type=%s ORDER BY modificationDate DESC LIMIT %s OFFSET %s"
_MYSQL_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
_GET_ITEM_COUNT_SQL = "SELECT COUNT(*) FROM items"
_GET_ITEM_COUNT_FILTERED_SQL = _GET_ITEM_COUNT_SQL + " WHERE type=%s"

class MySqlItemsDao(rpachallenge.scraping.dao.items.ItemsDao):
    def __init__(self):
        self.database = globals.config['mysql']['database'].get()
        self.user = globals.config['mysql']['user'].get()
    
        self.host = globals.config['mysql']['host'].get() if globals.config['mysql']['host'].exists() else "localhost"
        self.port = globals.config['mysql']['port'].get(int) if globals.config['mysql']['port'].exists() else 3306
        self.password = globals.config['mysql']['password'].get() if globals.config['mysql']['password'].exists() else None

        self._connect()

    def _connect(self):
        options = { 
            'host': self.host,
            'port': self.port,
            'user': self.user,
            'database': self.database    
        }

        if self.password:
            options['password'] = self.password

        self._connection = mysql.connector.connect(**options)
    
    def addItem(self, item):
        thread = threading.local()
        cursor = thread._current_cursor if hasattr(thread, "_current_cursor") else None
        single_action = cursor is None
        if single_action:
            cursor = self._connection.cursor()

        exception = True
        try:
            itemType = item.getItemType()
            cd = item.getCreationDate().strftime(_MYSQL_DATE_FORMAT)
            md = item.getModificationDate().strftime(_MYSQL_DATE_FORMAT)

            arguments = [
                item.getUrl(), itemType.name, item.getTitle(), item.getDescription(), cd, md
            ]

            cursor.execute(_ADD_ITEM_SQL, arguments)
            if single_action:
                self._connection.commit()

            exception = False
        finally:
            if single_action:
                try:
                    if exception:
                        self._connection.rollback()
                finally:
                    cursor.close()

    def addItems(self, items):
        thread = threading.local()
        thread._current_cursor = self._connection.cursor()

        exception = True
        try:
            super().addItems(items)
            exception = False
        finally:
            cursor = thread._current_cursor
            thread._current_cursor = None

            try:
                if exception:
                    self._connection.rollback()
                else:
                    self._connection.commit()
            finally:
                cursor.close()

    def clear(self, itemType):
        cursor = self._connection.cursor()

        exception = True
        try:
            cursor.execute(_DELETE_ITEMS_BY_TYPE, [ itemType.name ])
            exception = False
        finally:
            try:
                if exception:
                    self._connection.rollback()
                else:
                    self._connection.commit()
            finally:
                cursor.close()

    def clearAll(self):
        cursor = self._connection.cursor()

        exception = True
        try:
            cursor.execute(_DELETE_ALL_ITEMS)
            exception = False
        finally:
            try:
                if exception:
                    self._connection.rollback()
                else:
                    self._connection.commit()
            finally:
                cursor.close()

    def destroy(self):
        self._connection.close()

    def getItems(self, offset = 0, count = 100, itemType = None):
        args = [ count, offset ]
        if itemType:
            sql = _GET_ITEMS_FILTERED_SQL
            args.insert(0, itemType.name)
        else:
            sql = _GET_ITEMS_SQL

        results = []
        cursor = self._connection.cursor()

        try:
            cursor.execute(sql, args)

            for (url,itemType,title,description,creationDate,modificationDate) in cursor:
                it = ItemType[itemType]
                item = Item(it, url, title, description, creationDate, modificationDate)
                results.append(item)

        finally:
            cursor.close()

        return results

    def getItemsCount(self, itemType = None):
        if itemType:
            sql = _GET_ITEM_COUNT_FILTERED_SQL
            args = [ itemType.name ]
        else:
            sql = _GET_ITEM_COUNT_SQL
            args = []

        cursor = self._connection.cursor()
        try:
            cursor.execute(sql, args)
            for (count,) in cursor:
                return count
        finally:
            cursor.close()
