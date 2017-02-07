lextriecon
==========

'lextriecon' is a little implementation of a trie that I did for fun and for
practicing Python.
It's used to store words related to a specific subject. Each word may have a
description.

Why don't you have a look at the Wikipedia page below if you have no idea what a
trie is:
https://en.wikipedia.org/wiki/Trie


Repository content
------------------

- lextriecon.py: the module containing the 2 classes implementing the trie
- interface.py: a "command line user interface" using Pickle for persistence
- tests.py: the module containing all the tests


How does it work
----------------

In order to create/modify a trie:

1. clone this repository:

```sh
$ git clone git@github.com:eugenielm/lextriecon.git
```

2. Navigate to the repository

3. type the following command in the command line:

```sh
python interface.py <trie_name> <action> [word]
```

  The available actions are:
  - `list`, `empty`, `size` (no [word] after)
  - `find`, `add`, `remove`, `description`, `set_description` (followed by [word])

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
To run the tests from the command line, type `nosetests` inside this repository.
