import sys
from pprint import pprint
from .jisho import JishoHandler

jisho = JishoHandler()

def add_term(jisho_resp):
    print(jisho.get_japanese_term(jisho_resp))

def add_cards(col, config, tag, new_terms=[]):
    vocab_archive = [] #keeps record of added cards

    if new_terms:
        print(f"adding {len(new_terms)} new cards to {tag}")
        print(new_terms)
        # add a call to the card add function to the new_terms here
        for term in new_terms:
            jisho_resp = jisho.get_term_one(term)
            if not jisho_resp:
                print(f"\"{term}\" not found.")
            else: 
                add_term(jisho_resp)
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
            pprint(jisho_resp) #for testing

            print(" ------ ")
            print(f"Selected Term: {jisho.get_reading(jisho_resp)}")
            print(f"Part of Speech: {jisho.get_pos(jisho_resp)}")
            print(f"Definition: {jisho.get_definition(jisho_resp)}")
            print(" ------ ")
            add_note = input("Add term? (Y/n)")

            # take in no answer as yes
            if add_note is '':
                add_note = 'y'
            
            if add_note is 'y' or add_note is 'Y' or add_note is 'yes' or add_note is 'YES' or add_note is 'Yes':
                print ('its a yes')
                add_term(jisho_resp) #the logic to add the card