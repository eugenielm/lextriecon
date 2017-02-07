#-*- coding: UTF-8 -*-
import unittest
from lextriecon import Trie, Node

class NodeTest(unittest.TestCase):
    def setUp(self):
        self.root_node = Node(None, None)
        self.child = Node('e', self.root_node)
        self.gdchild = Node('t', self.child, is_word=True)
        self.gdchild2 = Node('n', self.child)
        self.gdgdchild = Node('a', self.gdchild)
        self.gdgdgdchild = Node('l', self.gdgdchild, is_word=True)

    def test_add_child(self):
        """Checks if it appends a child to a Node's children attribute"""
        self.assertIs(len(self.child.children), 0)
        self.child.add_child(self.gdchild)
        self.assertIs(len(self.child.children), 1)
        self.assertIs(self.child.children[0], self.gdchild)

    def test_get_last(self):
        """Checks if it returns a list of Node instances whose is_word attribute
        is set to True."""
        # First: need to set the children attributes of all the setUp Node instances
        self.child.add_child(self.gdchild)
        self.child.add_child(self.gdchild2)
        self.gdchild.add_child(self.gdgdchild)
        self.gdgdchild.add_child(self.gdgdgdchild)
        # Then it's possible to test the method:
        self.assertIs(type(self.child.get_last()), list)
        self.assertIs(len(self.child.get_last()), 2)
        self.assertIsInstance(self.gdchild.get_last()[0], Node)


class TrieTest(unittest.TestCase):
    def setUp(self):
        self.root_node = Node(None, None)
        self.test_trie = Trie(self.root_node)

    def test_insert_word(self):
        """Checks if it returns False if the word couldn't be inserted"""
        self.assertTrue(self.test_trie.insert_word("cerf-volant"))
        self.assertTrue(self.test_trie.insert_word("aujourd'hui"))
        self.assertTrue(self.test_trie.insert_word("crêpe"))
        self.assertFalse(self.test_trie.insert_word("cerf-volant"))
        self.assertIs(self.test_trie.insert_word("cerf@volant"), None)

    def test_get_size(self):
        """Checks if it returns the right integer"""
        self.assertIs(type(self.test_trie.get_trie_size()), int)
        self.assertIs(self.test_trie.get_trie_size(), 0)
        self.test_trie.insert_word('avocado')
        self.assertIs(self.test_trie.get_trie_size(), 1)
        self.test_trie.remove_word('avocado')
        self.assertIs(self.test_trie.get_trie_size(), 0)

    def test_find_word(self):
        """Checks if it returns False if the word isn't in the trie, otherwise return the last node"""
        self.assertFalse(self.test_trie.find_word("cerf-volant"))
        self.test_trie.insert_word("cerf-volant")
        self.assertIsInstance(self.test_trie.find_word("cerf-volant"), Node)
        self.assertIs(self.test_trie.find_word("cerf-volant").char, "t")

    def test_remove_word(self):
        """Checks if it returns True if the word could be removed"""
        self.test_trie.insert_word("cerf-volant")
        self.assertTrue(self.test_trie.remove_word("cerf-volant"))
        self.assertFalse(self.test_trie.remove_word("cerf-volant"))

    def test_list_words(self):
        """Checks if it returns a sorted list of unicode strings"""
        self.test_trie.insert_word("toutou")
        self.test_trie.insert_word("juju")
        self.assertIs(type(self.test_trie.list_words()), list)
        self.assertIs(type(self.test_trie.list_words()[0]), str)
        self.assertEqual(self.test_trie.list_words()[0], "juju")
        self.assertLess(self.test_trie.list_words()[0], self.test_trie.list_words()[1])

    def test_get_description(self):
        """Checks if it returns None or the description of a word, or False if
        the word isn't in the tree."""
        self.test_trie.insert_word("cerf-volant")
        self.assertFalse(self.test_trie.get_description("cerf"))
        self.assertIs(self.test_trie.get_description("cerf-volant"), None)
        self.test_trie.set_description("cerf-volant", "Flies high in the sky.")
        self.assertEqual(self.test_trie.get_description("cerf-volant"),
            "Flies high in the sky.")

    def test_set_description(self):
        """Checks if it sets the description of a word."""
        self.test_trie.insert_word("cerf-volant")
        self.assertIs(self.test_trie.get_description("cerf-volant"), None)
        self.test_trie.set_description("cerf-volant", "Flies high in the sky.")
        self.test_trie.set_description("cerf-volant", "Does it fly?")
        self.assertEqual(self.test_trie.get_description("cerf-volant"),
            "Flies high in the sky.")
        self.assertIs(self.test_trie.set_description("cerf", "Flies high in the sky."), None)
        self.assertFalse(self.test_trie.set_description("cerf-volant", "Does it fly?"))


if __name__ == '__main__':
    unittest.main()
