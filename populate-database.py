from rpachallenge.scraping.dao.mysql.dao import MySqlItemsDao
from rpachallenge.scraping.populate.google.engine import Engine
import rpachallenge.scraping.globals
from rpachallenge.scraping import Item, ItemType

rpachallenge.scraping.globals.initialize("rpa-search-results")
dao = MySqlItemsDao()
engine = Engine()

for itemType in ItemType:
    dao.clear(itemType)
    items = engine.getItems(itemType)
    dao.addItems(items)
