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

from rpachallenge.scraping.display.web.scraping_routing import ScrapingWebsite, setDAO
from rpachallenge.scraping.dao.mysql.dao import MySqlItemsDao
import rpachallenge.scraping.globals

rpachallenge.scraping.globals.initialize("rpa-search-results")
dao = MySqlItemsDao()
setDAO(dao)