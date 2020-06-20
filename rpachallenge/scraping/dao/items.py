
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
