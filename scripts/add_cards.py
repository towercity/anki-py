import sys
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

        if term is 'q':
            print('exiting...')
            searching = False
            pass