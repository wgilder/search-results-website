from rpachallenge.scraping.display.web.scraping_routing import ScrapingWebsite, setDAO
from rpachallenge.scraping.dao.mysql.dao import MySqlItemsDao
import rpachallenge.scraping.globals

rpachallenge.scraping.globals.initialize("rpa-search-results")
dao = MySqlItemsDao()
setDAO(dao)