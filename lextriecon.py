#-*- coding: UTF-8 -*-
# import re

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
    def __init__(self, char, parent=None, is_word=False):
        self.char = char
        self.parent = parent
        self.is_word = is_word
        self._children = []
        self.description = "" # is the empty string for all nodes whose is_word is False ; otherwise is either the empty string or not

    def get_char(self):
        """Return the value of the current node's char attribute."""
        return self.char

    def set_char(self, char):
        """Set the value of the current node's char attribute."""
        self.char = char

    def get_is_word(self):
        """Return a boolean value."""
        return self.is_word

    def set_is_word(self, bool):
        """Set the is_word attribute to True or False."""
        self.is_word = bool

    def get_parent(self):
        """Return a Node instance which is the preceding character of the word."""
        return self.parent

    @property
    def children(self):
        """Return a list of Node instances which can be empty."""
        return self._children

    def add_child(self, child):
        """Add a Node instance to the current node's children."""
        self.children.append(child)

    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description

    def get_last(self):
        """Return the list of all descendants whose is_word attribute is True."""
        last_letters = []
        if self.is_word: last_letters.append(self) # the current node is included
        if len(self.children) > 0:
            for child in self.children:
                last_letters.extend(child.get_last())
        return last_letters

class Trie(object):
    """A trie contains several words made of Node instances.
    After a word has been removed from the tree, useless nodes may remain in the
    tree, i.e nodes that aren't part of a word. These nodes may be used again
    later when adding new words.
    """
    def __init__(self, root):
        self.root = Node(None, parent=None, is_word=False) # the root node has None as a char value

    def get_trie_size(self):
        """Return the number of words in the trie (an integer)."""
        return len(self.list_words())

    def find_word(self, word):
        """Return False if the word couldn't be found, otherwise return its last node."""
        word = word.lower()
        if word.replace("'", "", 2).replace("-", "").decode('utf8').isalpha():
            current_node = self.root # we start at the root node of the tree
            while len(word) > 0:
                if len(current_node.children) == 0: # if the current node has no child
                    return False
                else: # if the current node has at least one child
                    if len(word) == 1:
                        for child in current_node.children:
                            if child.char == word and child.is_word:
                                return child # word found
                        return False
                    else: # if the word to insert has more than 1 character
                        identical = []
                        for child in current_node.children:
                            if child.char == word[0]:
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
                    if len(current_node.children) == 0:
                        new_child = Node(word, parent=current_node, is_word=True)
                        current_node.add_child(new_child)
                        return True # word inserted
                    else:# if the current node has got at least one child
                        for child in current_node.children:
                            if child.char == word and child.is_word:
                                return False# cannot insert word which is already in the tree
                            elif child.char == word and not child.is_word:
                                child.set_is_word(True)
                                return True # word inserted
                        # if the current node doesn't have a child whose char value equals word, then:
                        new_child = Node(word, parent=current_node, is_word=True)
                        current_node.add_child(new_child)
                        return True # word inserted

                else: # if the word has more than 1 character, we insert the 1st character
                    if len(current_node.children) == 0:
                        new_child = Node(word[0], parent=current_node)
                        current_node.add_child(new_child)
                        current_node = new_child
                        word = word[1:] # we make another loop after deleting the 1st letter that's just been inserted (=new_node)
                    else:
                        identical = []
                        for child in current_node.children:
                            if child.char == word[0]:
                                identical.append(child)
                        if len(identical) == 0:
                            new_child = Node(word[0], parent=current_node)
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
            last_node.description = "" # in case there was a description, delete it
            return True # word deleted
        else: return False # a word that's not in the tree cannot be removed

    def list_words(self):
        """Return a sorted list of all the words (strings) in the trie."""
        current_node = self.root
        if len(current_node.children) == 0:
            return []
        else: # make a list of of all ending letters (= all the nodes in the tree whose is_word value is True)
            my_list = []
            for child in current_node.children:
                my_list.extend(child.get_last())
        words = []
        for last in my_list: # for each ending letter, get the whole word by going up to the root node of the Tree
            current_node = last
            word = ""
            while current_node.char != None:# as long as we haven't reached the root node
                word += current_node.char
                current_node = current_node.parent
            word = word[::-1]#putting the letters into order
            words.append(word)
        words.sort()
        return words

    def set_description(self, word, description):
        """Return True if the description of a word could be added."""
        if description.replace(" ", "").replace(",", "").replace("'", "").\
        replace(".", "").replace(":", "").replace(";", "").replace("\\", "").\
        decode('utf8').isalnum() or description == "":
            last_node = self.find_word(word)
            try:
                last_node.description = description
                return True
            except: return None # the word isn't in the tree
        else: return False # the description must be alphanumeric characters (":", ";", "'", "-", ".", "," and " " are also accepted)

    def get_description(self, word):
        """Return the description of a word, None if it has no description, or
        False if the word isn't in the tree."""
        last_node = self.find_word(word)
        if last_node: # if the word is in the tree
            if len(last_node.description) == 0:
                return None
            else:
                return last_node.description # a string that isn't empty
        else: return False # the word isn't in the tree
