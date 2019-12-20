from pprint import pprint
import requests

class JishoHandler():
    JISHO_API = "https://jisho.org/api/v1/search/words?keyword="

    def get_term_all(self, search_term):
        url = "%s%s" % (self.JISHO_API, search_term)
        return requests.get(url).json()["data"]

    def get_term_one(self, search_term):
        jisho_resp = self.get_term_all(search_term)
        if jisho_resp:
            return jisho_resp[0] 
        else:
            return False

    def get_reading(self, jisho_resp): #returns term with [furigana]
        term_dict = jisho_resp['japanese'][0]
        if 'word' in term_dict:
            return ("%s[%s]" % (term_dict['word'], term_dict['reading']))
        else:
            return term_dict['reading']

    def get_definition(self, jisho_resp):
        senses = jisho_resp['senses'] # jisho gives each separate definition as a 'sense'
        sub_definitions = map(lambda sense: ', '.join(sense['english_definitions']), senses)
        definition = '; '.join(list(sub_definitions))
        return definition

    def get_japanese_term(self, jisho_resp):
        term_dict = jisho_resp['japanese'][0]
        if 'word' in term_dict:
            return term_dict['word']
        else:
            return term_dict['reading']

    def get_pos(self, jisho_resp):
        return jisho_resp['senses'][0]['parts_of_speech'][0]