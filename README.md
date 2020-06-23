# search-results-website
Simple flask-based website that displays search results. Initially designed as a website to test RPA scraping skills.

Installation:
* Requires Python 3
* Required Python packages: see requirements.txt
* MySQL database, with user with the following rights: DELETE, INSERT, SELECT
* A confuse configuration yaml file, with the following entries:
 * Map entry named mysql, with the following keys: host (default:localhost), port (default:3306), user (required), password (default: None), database (required)
 * Map entry named google, with the following keys: cseID, developerKey (see Google CSE)