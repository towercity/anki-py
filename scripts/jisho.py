import urllib.request as request
import json
from pprint import pprint

JISHO_API = "https://jisho.org/api/v1/search/words?keyword="

def get_term_all(search_term):
    url = "%s%s" % (JISHO_API, search_term)
    return json.loads(request.urlopen(url).read())["data"]

def get_term_one(search_term):
    jisho_resp = get_term_all(search_term)
    return jisho_resp[0] 

def get_reading(jisho_resp): #returns term with [furigana]
    term_dict = jisho_resp['japanese'][0]
    if 'word' in term_dict:
        return ("%s[%s]" % (term_dict['word'], term_dict['reading']))
    else:
        return term_dict['reading']


print(get_reading((get_term_one('red'))))