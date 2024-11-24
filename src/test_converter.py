
import unittest
from converter import text_node_to_html_node, split_nodes_delimiter
from textnode import TextNode, TextType

class TestConverter(unittest.TestCase):
    def test_text_node_to_html_node(self):
        text_node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {})

    def test_split_nodes_delimiter(self):
        old_nodes = [TextNode("This is a text node", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "*", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is a text node", TextType.TEXT)])

    
    def test_split_nodes_delimiter_with(self):
        old_nodes = [TextNode("This is a text node with a **bold** text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(
            new_nodes, 
            [
                TextNode("This is a text node with a ", TextType.TEXT), 
                TextNode("bold", TextType.BOLD), 
                TextNode(" text", TextType.TEXT)
            ]
        )
    
    def test_split_nodes_delimited_no_closing_delimiter(self):
        old_nodes = [TextNode("This is a text node with a **bold text", TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)