#-*- coding: UTF-8 -*-
import sys
import pickle
from lextriecon import Trie, Node


def check_input(args):
    """Checks if the command requirements have been met (eg: nb of args).
    This doesn't check if the [word] entered -if needed- contains only authorized
    characters"""
    actions = ['list', 'empty', 'size', 'add', 'remove', 'description', 'update_descriptions', 'find']
    if args[0] == 'new' and len(args) == 2 and args[1].isalnum():
        return True
    if args[1] not in actions:
        return False
    elif args[1] in actions[:3] and len(args) != 2:
        return False
    elif args[1] in actions[3:] and len(args) != 3:
        return False
    else: return True

args = list(sys.argv)[1:] # excluding the name of the program running
go_on = check_input(args)

if go_on:

    if args[0] == 'new':
        print
        try: # check if the lexicon the user wants to create already exist in the directory
            with open(args[1], "rb") as my_file:
                print "The lexicon you wanted to create already exists."
        except:
            my_lex = Trie(args[0])
            print "'%s' lexicon created." % args[1]


    else:
        print
        try: # check whether the lexicon the user wants to access already exist or not
            with open(args[0], "rb") as my_file:
                my_unpickle = pickle.Unpickler(my_file)
                my_lex = my_unpickle.load()
        except: # create an empty lexicon if it doesn't exist
            my_lex = Trie(args[0])
            print "'%s' lexicon didn't exist so it's been created." % args[0]


        if args[1] == 'list':
            words = my_lex.list_words()
            if words:
                print '%s contains the following word(s):' % args[0]
                for word in words:
                    print "-", word
            else:
                print "'%s' is empty." % args[0]


        elif args[1] == 'size':
            lex_size = my_lex.get_trie_size()
            if lex_size > 0:
                print "'%s' contains %i word(s)." % (args[0], lex_size)
            else:
                print "'%s' is empty." % args[0]


        elif args[1] == 'find':
            if my_lex.find_word(args[2]):
                print "%s is already in this lexicon." % args[2].lower()
            else:
                print "%s isn't in this lexicon." % args[2].lower()


        elif args[1] == 'add':
            res = my_lex.insert_word(args[2])
            if res:
                print "'%s' successfully inserted in this lexicon." % args[2].lower()
            elif res is None:
                print "The word couldn't be inserted because you typed in an unauthorized character."
            elif not res:
                print "The word couldn't be inserted because it's already in this lexicon."


        elif args[1] == 'remove':
            if my_lex.find_word(args[2]):
                confirmation = raw_input("Are you sure you want to delete '%s'? Y/N: " % args[2])
                if confirmation.upper() == 'Y' or confirmation.upper() == 'YES':
                    my_lex.remove_word(args[2])
                    print "Word successfully removed from this lexicon."
                else:
                    print "Deletion of '%s' cancelled." % args[2]
            else:
                print "The word couldn't be removed because it's not in this lexicon."


        elif args[1] == 'description':
            res = my_lex.get_word_descriptions(args[2])
            if res:
                print "Description(s) of %s:" % args[2]
                for name, content in res.items():
                    print "- %s: %s" % (name, content)
            elif res is None:
                print "There's no description in this lexicon for %s." % args[2]
            else:
                print "The word '%s' isn't in this lexicon." % args[2]


        elif args[1] == 'update_descriptions':
            word = my_lex.find_word(args[2])
            if not word:
                print "'%s' isn't in this lexicon." % args[2]
            else:
                if word.get_descriptions():
                    print "Here are the descriptions for %s: %s." % \
                    (args[2], ", ".join(["'%s'" % d for d in word.get_descriptions().keys()]))
                    print
                else:
                    print "This word has no description at the moment."
                    print
                
                choice = "0"
                while not (choice == "1" or choice == "2"):
                    choice = raw_input("Do you want to add/update(1) a description or delete(2) a description? -> ")

                if choice == "1":
                    descr_name = None
                    while not descr_name or not descr_name.isalnum():
                        descr_name = raw_input("Please type in the name of the description "\
                        "you want to update/add (alphanumeric char only):\n")
                
                    res = False

                    while not res:
                    
                        if not word.get_descriptions() or \
                        (word.get_descriptions() and descr_name not in word.get_descriptions().keys()):
                            descr_content = raw_input("Enter your description below:\n")
                            res = word.set_description(descr_name, descr_content)
                            if res:
                                print
                                print "'%s''s description successfully added." % args[2]
                            else:
                                print
                                print "The description couldn't be added because you used unauthorized characters."

                        else:
                            existing = word.get_descriptions()[descr_name]
                            print "The existing description is the following one:"
                            print "%s: %s" % (descr_name, existing)
                            print
                            answer = raw_input("Are you sure you want to change this description? Y/N: ")
                            if answer.upper() == 'Y' or answer.upper() == 'Y':
                                new_content = raw_input('Please type in the new content of your description:\n')
                                res = word.set_description(descr_name, new_content)
                                if res:
                                    print
                                    print "'%s''s description successfully updated." % args[2]
                                else:
                                    print
                                    print "The description couldn't be updated because you used unauthorized characters."
                            else:
                                print "Update canceled."
                                break

                else:
                    descr_name = False
                    while descr_name not in word.get_descriptions().keys():
                        descr_name = raw_input('Please type in the name of the description you want to delete (enter CTR+C to escape):\n')
                    word.remove_description(descr_name)
                    print "Description successfully deleted."


        elif args[1] == 'empty':
            confirmation = raw_input("Are you sure you want to empty '%s'? Y/N: " % args[0])
            if confirmation.upper() == 'Y' or confirmation.upper() == 'YES':
                my_lex = Trie(args[0])
                print "'%s' successfully emptied." % args[0]
            else:
                print "The deletion of '%s' was cancelled." % args[0]
        print

        with open(args[0], "wb") as my_file:
            my_pickler = pickle.Pickler(my_file)
            my_pickler.dump(my_lex)

else:
    print
    print "You entered invalid commands."
    print
    print "If you want to create a lexicon, please enter the following:"
    print "python interface.py new <trie_name>"
    print 
    print "If you want to update a lexicon, please enter the command below:"
    print "python interface.py <trie_name> <action> [word]"
    print
    print "- [word] must be typed in if (and only if) <action> is either 'add', "\
    "'remove', 'find', 'description' or 'update_descriptions'."
    print "- You are allowed to add a word containing a hyphen or an apostrophe "\
          "(preceded by a backslash), and also accented characters."
    print "- Nota Bene: if you want to add or remove a word containing a single quote, "\
          "you must escape it using a backslash."
    print
