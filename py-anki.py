import sys, os, json
from pprint import pprint
from scripts.change_cards import change_cards

# Load Anki library
sys.path.append("anki")
from anki.storage import Collection

# Load the config file
with open('config.json', 'r') as conf_file:
    config = json.load(conf_file)

# Define the path to the Anki SQLite collection
PROFILE_HOME = os.path.expanduser(config["collection_dir"]) 
cpath = os.path.join(PROFILE_HOME, "collection.anki2")

# Load the Collection
col = Collection(cpath, log=True) # Entry point to the API

change_cards(col, config)