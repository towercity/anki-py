from pprint import pprint
import requests

JISHO_API = "https://jisho.org/api/v1/search/words?keyword="

def get_term_all(search_term):
    url = "%s%s" % (JISHO_API, search_term)
    return requests.get(url).json()["data"]

def get_term_one(search_term):
    jisho_resp = get_term_all(search_term)
    return jisho_resp[0] 

def get_reading(jisho_resp): #returns term with [furigana]
    term_dict = jisho_resp['japanese'][0]
    if 'word' in term_dict:
        return ("%s[%s]" % (term_dict['word'], term_dict['reading']))
    else:
        return term_dict['reading']

def get_definition(jisho_resp):
    senses = jisho_resp['senses'] # jisho gives each separate definition as a 'sense'
    sub_definitions = map(lambda sense: ', '.join(sense['english_definitions']), senses)
    definition = '; '.join(list(sub_definitions))
    return definition