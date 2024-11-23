

import unittest

from src.htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("div", "Hello, World!")
        self.assertEqual(str(node), "HTMLNode(div, Hello, World!, [], {})")
    
    def test_repr_with_children(self):
        node = HTMLNode("div", children=[HTMLNode("p", "Hello, World!")])
        self.assertEqual(str(node), "HTMLNode(div, None, [HTMLNode(p, Hello, World!, [], {})], {})")


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "Hello, World!")
        self.assertEqual(node.to_html(), "<p>Hello, World!</p>")
    
    def test_to_html_with_props(self):
        node = LeafNode("p", "Hello, World!", {"class": "paragraph"})
        self.assertEqual(node.to_html(), '<p class="paragraph">Hello, World!</p>')
    
    def test_to_html_with_empty_value(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_to_html_with_no_tag(self):
        node = LeafNode(None, "Hello, World!")
        self.assertEqual(node.to_html(), "Hello, World!")