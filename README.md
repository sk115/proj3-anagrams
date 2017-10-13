# proj3-anagrams
Vocabularly anagrams game for primary school English language learners (ELL)

## Authors

* Carter Fritsch, cfritsch@uoregon.edu 
* Starter Code by M. Young

## Overview

A simple anagram game designed for English-language learning students in 
elementary and middle school.  
Students are presented with a list of vocabulary words (taken from a text file) 
and an anagram. The anagram is a jumble of some number of vocabulary words, randomly chosen. 
Students attempt to type vocabularly words that can be created from the jumble.  When a matching word is typed, it is added to a list of solved words.
The vocabulary word list is fixed for one invocation of the server, so multiple students connected to the same server will see the same vocabulary list but may have different anagrams.

## Composition

The application is composed of two parts:
* A flask server that serves the application pages and responds to AJAX Requests. The server holds a copy of the word list and jumble, and checks incoming input for matches
* An HTMl page that listens for events on a text input, then uses jQuery to make AJAX requests to the server to check the input for matches, handling the response by adding new-found words to the page and redirecting when the game has been won.

## Requirements

 * `python3`
 * `python3-venv`

## Starting the Application

* Copy `credentials-skel.ini` to the vocab directory as `credentials.ini`, alter for your use
* Run `make install` from the root directory
* Run `make start`


## Known bugs

The start/stop scheme is not working.  Flask (or perhaps the virtual
environment) is creating two Unix processes running the application,
and I am capturing the process ID for only one of them.  Therefore
stop.sh manages to kill only one, leaving the other running.  At this
time I do not know a workaround.  It is necessary to kill the second
process manually.  Use 'ps | grep python' to discover it, then 'kill'
to kill it.  Or, on Linux systems, use the 'killall' command. 

## Testing
* Use `nosetests`

There are currently nose tests for vocab.py, letterbag.py, and jumble.py. 

'make test' should work.  To run 'nosetests' explicitly, you must be
in the 'vocab' subdirectory. 

