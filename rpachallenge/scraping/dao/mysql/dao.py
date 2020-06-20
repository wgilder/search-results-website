
import rpachallenge.scraping.dao.items
import confuse
import mysql.connector
import threading
from rpachallenge.scraping import ItemType, Item

from rpachallenge.scraping import config

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
        config = confuse.Configuration('RpaChallengeScraping')

        self.host = config['mysql']['host'].get() if config['mysql']['host'].exists() else "localhost"
        self.port = config['mysql']['port'].get(int) if config['mysql']['port'].exists() else 3306
        self.user = config['mysql']['user'].get() if config['mysql']['user'].exists() else None
        self.password = config['mysql']['password'].get() if config['mysql']['password'].exists() else None
        self.database = config['mysql']['database'].get() if config['mysql']['database'].exists() else None

        self._connect()

    def _connect(self):
        options = {}
        if self.host:
            options['host'] = self.host

        if self.port:
            options['port'] = self.port

        if self.user:
            options['user'] = self.user

        if self.password:
            options['password'] = self.password

        if self.database:
            options['database'] = self.database    

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
            cursor.execute(_DELETE_ITEMS_BY_TYPE, itemType.name)
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
