import sys, os, json

# Load Anki library
sys.path.append("anki")
from anki.storage import Collection

# Define the path to the Anki SQLite collection
PROFILE_HOME = os.path.expanduser("~/.local/share/Anki2/User 1") 
cpath = os.path.join(PROFILE_HOME, "collection.anki2")

# Load the config file
with open('config.json', 'r') as conf_file:
    config = json.load(conf_file)

# Load the Collection
col = Collection(cpath, log=True) # Entry point to the API

# Use the available methods to list the notes

change_tag = config['tags']['change']

for cid in col.findNotes("tag:%s" % change_tag): 
    
    note = col.getNote(cid)
    front =  note.fields[2] # "Front" is the first field of these cards
    print(front)
