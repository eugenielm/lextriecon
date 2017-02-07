lextriecon
==========

'lextriecon' is a little implementation of a trie that I did for fun and for
practicing Python.
It's used to store words related to a specific subject. Each word may have a
description or not.

Why don't you have a look at the following Wikipedia page if you have no idea
what a trie is:
https://en.wikipedia.org/wiki/Trie


Repository content
------------------

- lextriecon.py: the module containing the 2 classes implementing the trie
- interface.py: a "command line user interface" using Pickle for persistence
- tests.py: the module containing all the tests


How does it work
----------------

In order to create/modify a trie:

1. Clone this repository:

  ```sh
  $ git clone git@github.com:eugenielm/lextriecon.git
  ```

2. Navigate to the repository

3. Type the following command in the command line:

  ```sh
  python interface.py <trie_name> <action> [word]
  ```

The available actions are:

+ no [word] after
  - `list`: display the list of the words in the trie
  - `empty`: empty the trie
  - `size`: show how many words are in the trie


+ followed by [word]
  - `find`: say if a word is in the trie or not
  - `add`: add a word in the trie
  - `remove`: remove a word from the trie
  - `description`: display a word's description
  - `set_description`: set a word's description


NB: You are allowed to add a [word] containing:
- one or several hyphens (-) ;
- an apostrophe (') (that must be preceded by a backslash if typed in the
  command line) ;
- accented characters (utf8 encoding is supported) ;
If using the command line, don't enter any special characters, especially the
following ones (which will either freeze it or raise an error):
```
< > ( ) " ' `
```


How to run the tests
--------------------
To run the tests from the command line, enter `nosetests` in the command line
when inside this repository.
