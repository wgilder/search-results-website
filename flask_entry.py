from rpachallenge.scraping.display.web.scraping_routing import ScrapingWebsite, setDAO
from rpachallenge.scraping.dao.mysql.dao import MySqlItemsDao

dao = MySqlItemsDao()
setDAO(dao)