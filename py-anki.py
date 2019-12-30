import sys, os, json, getopt
from pprint import pprint
from scripts.change_cards import change_cards
from scripts.add_cards import add_cards

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

# change_cards(col, config)
fullCmdArguments = sys.argv
argumentList = fullCmdArguments[1:]

unixOptions = "ha:c"
gnuOptions = ["help", "add=", "change",]

try:
    arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))
    sys.exit(2)

# evaluate given options
for currentArgument, currentValue in arguments:
    if currentArgument in ("-h", "--help"):
        print ("displaying help")
        print ("functionality coming soon...")
        sys.exit(0)
    elif currentArgument in ("-a", "--add"):
        add_cards(col, config, currentValue, values)
        sys.exit(0)
    elif currentArgument in ("-c", "--change"):
        change_cards(col, config)
