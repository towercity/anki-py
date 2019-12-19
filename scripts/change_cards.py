import sys, os, json
from pprint import pprint

# Load Anki library
sys.path.append("anki")
from anki.storage import Collection

# removes the change tag
def strip_tags(tags, change_tag):
    new_tags = filter(lambda tag: tag is not change_tag, tags)
    return list(new_tags)

def convert_note(note):
    term = note.fields[5] # pulls in the vocab term from the 'Note' field
    print(term)

# config is complete configutration dictionary
def change_cards(col, config):
    print('running subs change...')

    # short names for config dictionaries
    tags = config['tags']
    models = config['models']

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
        new_notes.append(convert_note(note))


# Define the path to the Anki SQLite collection
PROFILE_HOME = os.path.expanduser("~/.local/share/Anki2/User 1") 
cpath = os.path.join(PROFILE_HOME, "collection.anki2")

# Load the config file
with open('config.json', 'r') as conf_file:
    config = json.load(conf_file)

# Load the Collection
col = Collection(cpath, log=True) # Entry point to the API

change_cards(col, config)