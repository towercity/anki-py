import sys
from pprint import pprint
from .jisho import JishoHandler
from .change_cards import change_cards

jisho = JishoHandler()

def find_root(term, pos):
    term = list(term) #make a list for easy manipulations

    if pos == 'adjective' and term[len(term) - 1] == 'い':
        term = term[:-1] #remove the last character of the word
    elif pos == 'verb':
        term = term[:-1]
        
    return ''.join(term)

def add_term(jisho_resp, col, tag, config):
    term = jisho.get_japanese_term(jisho_resp)

    # check if not already exists; if so, add and leave
    note_exists = col.findNotes(f"Vocabulary:{term}")
    if note_exists:
        print(f"{term} already exists in database. Adding tag {tag}...")
        col.tags.bulkAdd(note_exists, tag, True) #the actual adding logic for anki 
        return True

    print(f"{term} does not yet exist")

    # find root term for better quality searching
    term_root = find_root(term, jisho.get_pos(jisho_resp))
    print('Searching for notes in database with term...')
    subs2srs_notes = col.findNotes(f"note:{config['models']['subs2srs']} {term_root}")

    if subs2srs_notes: #if it's found something....
        print('Note found!\nPreparing note')
        edit_notes = subs2srs_notes[0:1]
        note = col.getNote(subs2srs_notes[0]) #only edit the first found note
        note.fields[5] = term #saves the term to the correct field in the model
        col.tags.bulkAdd(edit_notes, config["tags"]["change"], True) #mark it to change 
        col.tags.bulkAdd(edit_notes, tag, True) #add the new tag
        note.flush()
    else:
        print('No notes found.\nAdding new card...')

        # Set the model
        modelBasic = col.models.byName(config["models"]["japanese"])
        col.decks.current()['mid'] = modelBasic['id']

        # Get the deck
        deck = col.decks.byName(config["decks"]["main"])

        # Instantiate the new note
        note = col.newNote()
        note.model()['did'] = deck['id']

        # Add the fields
        note.fields[0] = term
        note.fields[1] = jisho.get_reading(jisho_resp)
        note.fields[3] = jisho.get_definition(jisho_resp) 

        # Set the tags (and add the new ones to the deck configuration
        note.tags = col.tags.canonify(col.tags.split(tag))
        m = note.model()
        m['tags'] = note.tags
        col.models.save(m)

        # Add the note
        col.addNote(note)

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
                add_term(jisho_resp, col, tag, config)
                vocab_archive.append(term)
    else:
        print(f"adding new cards to {tag}")

    # start notes add loop
    searching = True
    while searching:
        term = input("Enter term or 'q' to quit: ")

        # exit condition
        if term == 'q':
            print('exiting...')
            searching = False
            break

        # pull data from jisho        
        jisho_resp = jisho.get_term_one(term)
        if not jisho_resp:
            print('No term found. rerunning search')
            print(" ------ ")
        else:
            term = jisho.get_japanese_term(jisho_resp)

            print(" ------ ")
            print(f"Selected Term: {jisho.get_reading(jisho_resp)}")
            print(f"Part of Speech: {jisho.get_pos(jisho_resp)}")
            print(f"Definition: {jisho.get_definition(jisho_resp)}")
            print(" ------ ")
            add_note = input("Add term? (Y/n): ")

            # take in no answer as yes
            if add_note == '':
                add_note = 'y'
            
            if add_note == 'y' or add_note == 'Y' or add_note == 'yes' or add_note == 'YES' or add_note == 'Yes':
                add_term(jisho_resp, col, tag, config) #the logic to add the cardo
                print(f"added {term}")
                vocab_archive.append(term)            

        print(f"current archive: {' '.join(vocab_archive)}")

    print('Copying over subs2srs notes...')
    change_cards(col, config)

    print('saving to database')
    col.save()
