# anki-py: a very basic anki command line tool

`anki-py` is a simple python3-based command line interface for Anki. It runs a few basic deck management scripts now, with plans to add more. Best of all, it's easily extensible, so adding your own scripts is a cinch.

This is adapted from my earlier node-based [anki-cli](https://github.com/towercity/anki-cli) anki client, becuase writing a node-based client for python software is needlessly complex.

Also worth noting: I developed this for use with Japanese study. It'd probably be very easy to adapt the code to your own use, but if you're studying Japanese then, hey. That works out.

## Installation

1. clone the repo to your machine
2. that's it

## Use

As of now, `anki-py` is nothing more than a wrapper around a bunch of basic anki management script I make use of. To run them, simply run `py-anki.py` from the root directory with python3 with the appropriate command flag from the list below.

## Scripts


### change: `-c | -change`

This is a script I use to convert subs2srs cards into regular Japanese review study cards. To use:

1. copy the new term you'd like to make a card for into the Note field of your subs2srs card
2. tag the card with the change tag you've set in `/config.json` (defaults to `00change`)
3. run `python py-anki.py -c`

The script will automatically change the subs2srs card into a vocab card and move it into the proper deck (which you can change in the decks subobject of `config.json`). It can handle any number of changes in one call, so it helps to have a lot built up

### add: `-a tag_name | --add tag_name`

adds new vocabulary study cards to the specified tag_name.

My main reason for building this program: this script is a quick and easy (therefore entirely imperfect) little script that lets you search jisho for the meanings of Japanese terms and add them to your Anki database.

In essence, this is an all-in-one reading practice app, stripped to its barest bits. You select a tag you'd like to add cards to -- I use the name of whatever game/book/article I'm reading here, for easy filtered decks later -- then the script will continually prompt you for new words to search the meanings of, until you tell it to quit, that is. It will display the word you've searched with its definition, then prompt if you'd like to add the card to your Anki database or not.

If you select yes, the script will search for the term in your database. If a noot already exists, it will add the tag you've selected to the note than continue the loop. If the card doesn't exist, it will then search your subs2srs cards for any notes that uses the term (with some very basic conjugation allowances), add the tag you've selected to the card, convert the card to a standard Vocabulary card, then continue the loop. (Note: see above for how the script uses subs2srs -- the script uses the cahnge script described above for this functionality.) Finally, if none of these methods find any notes, the script will create a new card for the term with the tag you've chosen. It'll also tell you how many notes you've added so far. Why? I don't know, I guess it just helps you feel accomplished.

