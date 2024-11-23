

import unittest

from src.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("div", "Hello, World!")
        self.assertEqual(str(node), "HTMLNode(div, Hello, World!, [], {})")
    
    def test_repr_with_children(self):
        node = HTMLNode("div", children=[HTMLNode("p", "Hello, World!")])
        self.assertEqual(str(node), "HTMLNode(div, None, [HTMLNode(p, Hello, World!, [], {})], {})")