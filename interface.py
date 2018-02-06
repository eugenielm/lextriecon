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
            if len(my_lex) > 0:
                words = my_lex.list_words()
                print '%s contains the following word(s):' % args[0]
                for word in words:
                    print "-", word
            else:
                print "'%s' is empty." % args[0]


        elif args[1] == 'size':
            if len(my_lex) > 1:
                print "'%s' contains %i words." % (args[0], len(my_lex))
            elif len(my_lex) == 1:
                print "'%s' contains 1 word." % args[0]
            else:
                print "'%s' is empty." % args[0]


        elif args[1] == 'find':
            if args[2] in my_lex:
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
                    print "'%s' successfully removed from this lexicon." % args[2]
                else:
                    print "Deletion of '%s' was cancelled." % args[2]
            else:
                print "'%s' couldn't be removed because it's not in this lexicon." % args[2]


        elif args[1] == 'description':
            if args[2] not in my_lex:
                print "'%s' isn't in %s." % (args[2], args[0])
            elif my_lex[args[2]]:
                print "Description(s) of '%s':" % args[2]
                for name, content in my_lex[args[2]].items():
                    print "- %s: %s" % (name, content)
            else:
                print "There's no description in this lexicon for '%s'." % args[2]


        elif args[1] == 'update_descriptions':
            if args[2] not in my_lex:
                print "'%s' isn't in this lexicon." % args[2]
            else:
                choice = "0"
                if my_lex[args[2]]:
                    print "Here are the descriptions for '%s': %s." % \
                    (args[2], ", ".join(["'%s'" % d for d in my_lex[args[2]]]))
                    print
                else:
                    print "'%s' has no description at the moment." % args[2]
                    choice = "1"
                    print
                
                while not (choice == "1" or choice == "2" or choice == 'exit' or choice == 'EXIT'):
                    choice = raw_input("Do you want to 1- add/update a description or 2- delete a description?"+\
                    "\n(otherwise type in 'exit')\n-> ")

                if choice == 'exit':
                    print

                elif choice == "1":
                    descr_name = None
                    while not descr_name or not descr_name.replace("_", "").decode('utf8').isalnum():
                        descr_name = raw_input("Please type in the name of the description "+\
                        "you want to add or update (alphanumeric chars and underscores only):\n")
                
                    res = False

                    while not res:
                    
                        if not my_lex[args[2]] or \
                        (my_lex[args[2]] and descr_name not in my_lex[args[2]]):
                            descr_content = raw_input("Enter your description below:\n")
                            res = my_lex.set_word_description(args[2], descr_name, descr_content)
                            if res:
                                print
                                print "'%s''s description successfully added." % args[2]
                            else:
                                print
                                print "The description couldn't be added because you used unauthorized characters."

                        else:
                            existing = my_lex[args[2]][descr_name]
                            print
                            print "The existing description is the following one:"
                            print "%s: %s" % (descr_name, existing)
                            print
                            answer = raw_input("Are you sure you want to change this description? Y/N: ")
                            if answer.upper() == 'Y' or answer.upper() == 'Y':
                                new_content = raw_input('Please type in the new content of your description:\n')
                                res = my_lex.set_word_description(args[2], descr_name, new_content)
                                if res:
                                    print
                                    print "'%s''s description successfully updated." % args[2]
                                else:
                                    print
                                    print "The description couldn't be updated because you used unauthorized characters."
                            else:
                                print
                                break

                else:
                    descr_name = raw_input("Please type in the name of the description you want to delete "+\
                    "(Nota Bene: description names are case sensitive).\nType 'exit' to quit:\n")
                    print
                    if descr_name == 'exit':
                        print "Deletion cancelled."
                    elif descr_name in my_lex[args[2]]:
                        my_lex.remove_word_description(args[2], descr_name)
                        print "Description successfully deleted."
                    else:
                        print "Cannot delete a description that's not here..."


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
