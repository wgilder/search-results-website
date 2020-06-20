
from googleapiclient.discovery import build

import pprint
import re

__KEY__='AIzaSyDEujTqUs6-sIDQCHxlITcT6U8oRlAFEZg'
__CX__='003648246807547447764:vejoc3ypqqe'

def main():
  td = re.compile("((19[89]\d)|(20[01]\d)|(2020))") 
  service = build("customsearch", "v1", developerKey=__KEY__)
  offset = 1
  total = 0
  totalWithDate = 0
  first = True

  print("")
  print("")
  print("")
  print("")
  print("")
  print("")
  print("")
  print("START*START*START*START*START*START*START*START*START*START*START*START*START*START*START")
  print("START*START*START*START*START*START*START*START*START*START*START*START*START*START*START")
  print("START*START*START*START*START*START*START*START*START*START*START*START*START*START*START")
  print("")

  for x in range(10):
    res = service.cse().list(q='process automation', cx=__CX__, siteSearch='youtube.com', start=offset, excludeTerms="channel").execute()
    # res = service.cse().list(q='process automation', cx=__CX__, fileType="doc", start=offset).execute()
    if 'nextPage' in res['queries']:
      offset = res['queries']['nextPage'][0]['startIndex']
    else:
      offset = -1

    for item in res['items']:
      if first:
        first = False
      else:
        print("####################################")
      print(item['link'])
      total = total + 1
      if 'pagemap' in item:
        found = False
        for pm in item['pagemap'].items():
          pmKey = pm[0]
          for l in pm[1]:
            for tags in l.items():
              if td.search(tags[1]):
                print(pmKey + "/" + tags[0] + ":" + tags[1])
                if not found:
                  found = True
                  totalWithDate = totalWithDate + 1
        if not found:
          pprint.pprint(item['pagemap'])
      else:
        print ("**********No Pagemap***********")
        pprint.pprint(item)

    if offset < 0:
      break

  print("total results: {:d}".format(total))
  print("count with dates: {:d}".format(totalWithDate))

        
  # items = res["items"]
#  for x in items:
#      print("title: " + x['title'] + " (" + x['link'] + ")")
#  pprint.pprint(res)
  # pprint.pprint(items[0])

if __name__ == '__main__':
  main()

# https://customsearch.googleapis.com/customsearch/v1?q=process%20automation&cx=003648246807547447764%3Avejoc3ypqqe&key=AIzaSyDEujTqUs6-sIDQCHxlITcT6U8oRlAFEZg&alt=json&fields=queries(nextPage/startIndex),items(title,link,snippet)&prettyPrint=true&fileType=doc