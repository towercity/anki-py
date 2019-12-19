import urllib.request as request
import json
from pprint import pprint

JISHO_API = "https://jisho.org/api/v1/search/words?keyword="

def get_all(search_term):
    url = "%s%s" % (JISHO_API, search_term)
    return json.loads(request.urlopen(url).read())["data"]

def get_one(search_term):
    jish_resp = get_all(search_term)
    return jish_resp[0] 

alls = get_all('red')
print("%s: all" % len(alls))
