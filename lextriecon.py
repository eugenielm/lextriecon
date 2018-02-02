#-*- coding: UTF-8 -*-

"""

This module contains 2 classes:
- the Node class whose instances represent one character of a word ;
- the Trie class whose instances are collections of words, which are
themselves made of Node instances.

"""

class Node(object):
    """Each node represents a character of a word.

    Each node has only one parent and can have zero, one or more children.
    A node whose is_word attribute is set to True is the last character of a word.
    A char attribute, i.e. a character of a word, can be any alphabetic character
    (even accented), a hyphen (-) or an apostrophe (').

    """
    def __init__(self, char, parent, is_word=False):
        self.char = char
        self.parent = parent
        self.is_word = is_word
        self.children = []
        # if they exist, descriptions are bound to the last character of a word only
        self.descriptions = {}

    def get_char(self):
        return self.char

    def get_is_word(self):
        return self.is_word

    def set_is_word(self, boolean):
        self.is_word = boolean

    def get_parent(self):
        return self.parent

    def set_parent(self, new_parent):
        self.parent = new_parent

    def get_children(self):
        return self.children

    def add_child(self, new_child):
        self.children.append(new_child)

    def get_last(self):
        """Return the list of all descendants whose is_word attribute is True."""
        last_letters = []
        if self.is_word: last_letters.append(self) # the current node is included
        if len(self.children) > 0:
            for child in self.children:
                last_letters.extend(child.get_last())
        return last_letters

    def get_descriptions(self):
        return self.descriptions

    def set_description(self, descr_name, descr_content):
        """Return True if the description could be set - otherwise return False.
        The following punctuation signs and special characters are accepted in
        the description:
        , ' . : ; \ - as well as white spaces and numbers."""
        if descr_content.replace(" ", "").replace(",", "").replace("'", "").\
           replace(".", "").replace(":", "").replace(";", "").replace("\\", "").\
           replace("-", "").decode('utf8').isalnum() and descr_name.decode('utf8').isalnum():
            self.descriptions[descr_name] = descr_content
            return True
        return False

    def remove_description(self, descr_name):
        try:
            del self.descriptions[descr_name]
            return True
        except KeyError:
            return False

    def delete_all_descriptions(self):
        self.descriptions = {}


class Trie(object):
    """A trie contains several words made of Node instances.
    After a word has been removed from the tree, useless nodes may remain in the
    tree, i.e nodes that aren't part of a word. These nodes may be used again
    later when adding new words.
    """
    def __init__(self, name):
        self.name = name
        self.root = Node(None, None) # the root node has None as a char value and as a parent

    def get_trie_size(self):
        """Return the number of words in the trie (an integer)."""
        return len(self.list_words())

    def find_word(self, word):
        """Return False if the word couldn't be found, otherwise return its last node."""
        if not self.root: return False

        word = word.lower()
        if word.replace("'", "", 2).replace("-", "").decode('utf8').isalpha():
            current_node = self.root # we start at the root node of the tree
            while len(word) > 0:
                if len(current_node.get_children()) == 0: # if the current node has no child
                    return False
                else: # if the current node has at least one child
                    if len(word) == 1:
                        for child in current_node.get_children():
                            if child.get_char() == word and child.get_is_word():
                                return child # word found
                        return False
                    else: # if the word to insert has more than 1 character
                        identical = []
                        for child in current_node.get_children():
                            if child.get_char() == word[0]:
                                identical.append(child)
                        if len(identical) == 0: return False # word not found
                        else:
                            current_node = identical[0]
                            word = word[1:]
        else: return False

    def insert_word(self, word):
        """Return True if the word could be inserted (as a unicode string)."""
        word = word.lower()
        if self.find_word(word): # cannot insert a word which is already in the tree
            return False

        if word.replace("'", "", 2).replace("-", "").decode('utf8').isalpha():
            current_node = self.root # we start at the root node
            while len(word) > 0:
                if len(word) == 1: # last loop
                    if len(current_node.get_children()) == 0:
                        new_child = Node(word, current_node, is_word=True)
                        current_node.add_child(new_child)
                        return True # word inserted
                    else: # if the current node has got at least one child
                        for child in current_node.get_children():
                            if child.get_char() == word and child.get_is_word():
                                return False # cannot insert word which is already in the tree
                            elif child.get_char() == word and not child.get_is_word():
                                child.set_is_word(True)
                                return True # word inserted
                        # if the current node doesn't have a child whose char value equals word
                        new_child = Node(word, current_node, is_word=True)
                        current_node.add_child(new_child)
                        return True # word inserted

                else: # if the word has more than 1 character, we insert the 1st character
                    if len(current_node.get_children()) == 0:
                        new_child = Node(word[0], current_node)
                        current_node.add_child(new_child)
                        current_node = new_child
                        word = word[1:] # we make another loop after deleting the 1st letter that's just been inserted (=new_node)
                    else:
                        identical = []
                        for child in current_node.get_children():
                            if child.get_char() == word[0]:
                                identical.append(child)
                        if len(identical) == 0:
                            new_child = Node(word[0], current_node)
                            current_node.add_child(new_child)
                            current_node = new_child
                            word = word[1:]
                        else:
                            current_node = identical[0]
                            word = word[1:]

        else: return None

    def remove_word(self, word):
        """Return True if the word could be removed, return False otherwise."""
        last_node = self.find_word(word)
        if last_node:
            last_node.set_is_word(False)
            # in case there were descriptions, delete them
            last_node.delete_all_descriptions()
            return True # word deleted
        else: return False # a word that's not in the tree cannot be removed

    def list_words(self):
        """Return a sorted list of all the words (strings) in the trie."""
        current_node = self.root
        if len(current_node.get_children()) == 0:
            return []
        else: # make a list of of all ending letters (= all the nodes in the tree whose is_word value is True)
            my_list = []
            for child in current_node.get_children():
                my_list.extend(child.get_last())
        words = []
        for last in my_list: # for each ending letter, get the whole word by going up to the root node of the Tree
            current_node = last
            word = ""
            while current_node.get_char() != None: # as long as we haven't reached the root node
                word += current_node.get_char()
                current_node = current_node.get_parent()
            word = word[::-1] # putting the letters into order
            words.append(word)
        words.sort()
        return words

    def set_word_description(self, word, descr_name, descr_content):
        """Return True if the description of a word could be added.
        Return None if the word isn't in the tree, and False if the description couldn't be added.
        """
        last_node = self.find_word(word) # check if the word is in the tree
        if not last_node: return None

        if last_node.set_description(descr_name, descr_content):
            return True
        else:
            return False # the description contains unauthorized characters

    def remove_description(self, word, descr_name):
        """Return True if the description could be removed, False otherwise."""
        last_node = self.find_word(word)
        if last_node and last_node.get_descriptions():
            try:
                last_node.remove_description(descr_name)
                return True
            except KeyError:
                return False
        return False

    def get_word_descriptions(self, word):
        """Return the descriptions of a word, None if it has no description, or
        False if the word isn't in the tree."""
        last_node = self.find_word(word)
        if last_node: # if the word is in the tree
            if not last_node.get_descriptions():
                return None
            else:
                return last_node.get_descriptions() # a dict that isn't empty
        else: return False # the word isn't in the tree
