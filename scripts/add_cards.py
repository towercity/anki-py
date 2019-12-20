import sys
from pprint import pprint
from .jisho import JishoHandler

jisho = JishoHandler()

def add_cards(col, config, tag, new_terms=[]):
    vocab_archive = [] #keeps record of added cards

    if new_terms:
        print(f"adding {len(new_terms)} new cards to {tag}")
        print(new_terms)
        # add a call to the card add function to the new_terms here
    else:
        print(f"adding new cards to {tag}")

    # start notes add loop
    searching = True
    while searching:
        term = input("Enter term or 'q' to quit: ")

        # exit condition
        if term is 'q':
            print('exiting...')
            searching = False
            break

        # pull data from jisho        
        jisho_resp = jisho.get_term_one(term)
        if not jisho_resp:
            print('No term found. rerunning search')
        else:
            term = jisho.get_japanese_term(jisho_resp) #overwrites entered variable