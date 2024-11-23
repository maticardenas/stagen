

import unittest
from converter import text_node_to_html_node
from textnode import TextNode, TextType

class TestConverter(unittest.TestCase):
    def test_text_node_to_html_node(self):
        text_node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {})