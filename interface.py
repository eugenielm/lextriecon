#-*- coding: UTF-8 -*-
import sys
import pickle
from lextriecon import Trie, Node


def check_input(args):
    """Checks if the command requirements have been met (eg: nb of args).
    This doesn't check if the [word] entered -if needed- contains only authorized
    characters"""
    if args[1] != 'list' and args[1] != 'add' and args[1] != 'remove' and \
       args[1] != 'empty' and args[1] != 'size' and args[1] != 'description' and \
       args[1] != 'set_description' and args[1] != 'find':
        return False
    elif (args[1] == 'list' or args[1] == 'empty' or args[1] == 'size') and len(args) != 2:
        return False
    elif (args[1] == 'add' or args[1] == 'remove' or args[1] == 'description' or \
          args[1] == 'set_description') and len(args) != 3:
        return False
    else: return True

args = list(sys.argv)[1:] # excluding the name of the program
go_on = check_input(args)

if go_on:
    try:# check whether the tree the user wants to access already exist or not
        with open(args[0], "rb") as my_file:
            my_unpickle = pickle.Unpickler(my_file)
            my_lex = my_unpickle.load()
    except:# create an empty tree if it doesn't exist
        my_lex = Trie()

    if args[1] == 'list':
        words = my_lex.list_words()
        if words:
            print '%s contains the following words:' % args[0]
            for word in words:
                print word
        else:
            print "The tree is empty."

    elif args[1] == 'size':
        lex_size = my_lex.get_trie_size()
        if lex_size > 0:
            print '%s contains %i words' % (args[0], lex_size)
        else:
            print "The tree is empty."

    elif args[1] == 'find':
        if my_lex.find_word(args[2]):
            print "%s is already in the tree." % args[2].lower()
        else:
            print "%s isn't in the tree." % args[2].lower()

    elif args[1] == 'add':
        res = my_lex.insert_word(args[2])
        if res:
            print "'%s' successfully inserted in the tree." % args[2].lower()
        elif res is None:
            print "The word couldn't be inserted because you typed in an unauthorized character."
        elif not res:
            print "The word couldn't be inserted because it's already in the tree."

    elif args[1] == 'remove':
        if my_lex.remove_word(args[2]):
            print "Word successfully removed from the tree."
        else:
            print "The word couldn't be removed because it's not in the tree."

    elif args[1] == 'description':
        res = my_lex.get_description(args[2])
        if res:
            print res
        elif res is None:
            print "There's no description set for this word."
        else:
            print "The word isn't in the tree."

    elif args[1] == 'set_description':
        description = raw_input('Please type in your description:\n')
        res = my_lex.set_description(args[2], description)
        if res:
            print "'%s''s description successfully updated." % args[2]
        elif res is None:
            print "The word isn't in the tree."
        else:
            print "The description couldn't be added because you used unauthorized characters."

    elif args[1] == 'empty':
        my_lex = Trie()
        print "Tree emptied."

    with open(args[0], "wb") as my_file:
        my_pickler = pickle.Pickler(my_file)
        my_pickler.dump(my_lex)

else:
    print
    print "You entered invalid commands."
    print "Please enter the command below:"
    print "'python interface.py <trie_name> <action> [word]' (don't use quotes)"
    print "[word] must be typed in if (and only if) <action> is either 'add', "\
    "'remove', 'find', 'description' or 'set_description'."
    print "You are allowed to add a word containing a hyphen or an apostrophe "\
          "(preceded by a backslash), and also accented characters."
    print "NB: if you want to add or remove a word containing a single quote, "\
          "you must escape it using a backslash."
    print
