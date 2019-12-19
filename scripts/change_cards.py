import sys, os, json
from pprint import pprint
import jisho

# Load Anki library
sys.path.append("anki")
from anki.storage import Collection

# removes the change tag
def strip_tags(tags, change_tag):
    tags.remove(change_tag)
    return tags

def create_new_note(note, model, deck, tags):
    term = note.fields[5] # pulls in the vocab term from the 'Note' field
    print(f"attempting {term}....")
    jisho_resp = jisho.get_term_one(term) # pulls info from Jisho
    print('info found!')

    new_note = {
        "deckName": deck,
        "modelName": model,
        "fields": {
            "Vocabulary": term,
            "Vocabulary-Reading": jisho.get_reading(jisho_resp),
            "Meaning": jisho.get_definition(jisho_resp),
            "Sentence-1-Audio": note.fields[0],
            "Sentence-1-Image": note.fields[1],
            "Sentence-1": note.fields[2],
            "Sentence-1-English": note.fields[3],
            "Sentence-1-Reading": note.fields[4],
        },
        "tags": strip_tags(note.tags, tags['change'])
    }

    return new_note
    
def send_to_anki(new_note, col):
    # Set the model
    modelBasic = col.models.byName(new_note['modelName'])
    col.decks.current()['mid'] = modelBasic['id']

    # Get the deck
    deck = col.decks.byName(new_note['deckName'])

    # Instantiate the new note
    note = col.newNote()
    note.model()['did'] = deck['id']

    # Add the fields
    new_field = new_note['fields']
    note.fields[0] = new_field['Vocabulary']
    note.fields[1] = new_field['Vocabulary-Reading']
    note.fields[3] = new_field['Meaning']
    note.fields[7] = new_field['Sentence-1']
    note.fields[8] = new_field['Sentence-1-Reading']
    note.fields[10] = new_field['Sentence-1-English']
    note.fields[11] = new_field['Sentence-1-Audio']
    note.fields[12] = new_field['Sentence-1-Image']

    # Print Note Info
    print(f"new note\nterm: {note.fields[0]}\nmeaning: {note.fields[3]}\n")

    # Set the tags (and add the new ones to the deck configuration
    tags = " ".join(new_note["tags"])
    note.tags = col.tags.canonify(col.tags.split(tags))
    m = note.model()
    m['tags'] = note.tags
    col.models.save(m)

    # Add the note
    col.addNote(note)

# config is complete configutration dictionary
def change_cards(col, config):
    print('running subs change...')

    # short names for config dictionaries
    tags = config['tags']
    models = config['models']
    decks = config['decks']

    print('gathering notes...')

    # search the database for subs cards tagged to change
    noteIds = col.findNotes("tag:%s" % tags['change'])

    # check for blank notes array; if empty, return False
    if not len(noteIds):
        print('error: no notes found')
        return False
    
    print("%s notes gathered\ncreating new notes..." % len(noteIds))

    new_notes = [] #blank array to hold new notes made below
    # create the notes
    for noteId in noteIds:
        note = col.getNote(noteId)
        new_notes.append(create_new_note(note, model=models['japanese'], deck=decks['main'], tags=tags))
    
    print(f"...\ncreated {len(new_notes)} new notes\nsending to Anki...\n")

    for new_note in new_notes:
        send_to_anki(new_note, col)
        # pass
    
    print('deleting old notes...')
    col.remNotes(noteIds)

    print('saving to database...')
    col.save()
    print('changes saved!\nplease open anki desktop to sync')

# Define the path to the Anki SQLite collection
PROFILE_HOME = os.path.expanduser("~/.local/share/Anki2/User 1") 
cpath = os.path.join(PROFILE_HOME, "collection.anki2")

# Load the config file
with open('config.json', 'r') as conf_file:
    config = json.load(conf_file)

# Load the Collection
col = Collection(cpath, log=True) # Entry point to the API

change_cards(col, config)