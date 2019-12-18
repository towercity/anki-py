import urllib.request as request
import json
from pprint import pprint

JISHO_API = "https://jisho.org/api/v1/search/words?keyword="

def get_json(search_term):
    url = "%s%s" % (JISHO_API, search_term)
    return json.loads(request.urlopen(url).read())

pprint(get_json('red'))