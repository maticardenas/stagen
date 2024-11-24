
import unittest
from converter import split_node_images, split_node_links, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links
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

    def test_extract_markdown_images(self):
        text = "This is a text with an image ![alt text](https://example.com/image.png)"
        images = extract_markdown_images(text)
        self.assertEqual(images, [("alt text", "https://example.com/image.png")])

    def test_extract_markdown_links(self):
        text = "This is a text with a link [link text](https://example.com)"
        links = extract_markdown_links(text)
        self.assertEqual(links, [("link text", "https://example.com")])

    def test_split_node_images(self):
        old_nodes = [TextNode("This is a text with an image ![alt text](https://example.com/image.png)", TextType.TEXT)]
        new_nodes = split_node_images(old_nodes)
        self.assertEqual(
            new_nodes, 
            [
                TextNode("This is a text with an image ", TextType.TEXT), 
                TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"), 
            ]
        )

    def test_split_node_images_multiple_images(self):
        old_nodes = [TextNode("This is a text with an image ![alt text](https://example.com/image.png) and another ![alt text 2](https://example.com/image2.png)", TextType.TEXT)]
        new_nodes = split_node_images(old_nodes)
        self.assertEqual(
            new_nodes, 
            [
                TextNode("This is a text with an image ", TextType.TEXT), 
                TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"), 
                TextNode(" and another ", TextType.TEXT), 
                TextNode("alt text 2", TextType.IMAGE, "https://example.com/image2.png"), 
            ]
        )
    
    def test_split_node_images_no_image(self):
        old_nodes = [TextNode("This is a text with no image", TextType.TEXT)]
        new_nodes = split_node_images(old_nodes)
        self.assertEqual(new_nodes, [TextNode("This is a text with no image", TextType.TEXT)])

    
    def test_split_node_links(self):
        old_nodes = [TextNode("This is a text with a link [link text](https://example.com)", TextType.TEXT)]
        new_nodes = split_node_links(old_nodes)
        self.assertEqual(
            new_nodes, 
            [
                TextNode("This is a text with a link ", TextType.TEXT), 
                TextNode("link text", TextType.LINK, "https://example.com"), 
            ]
        )
    
    def test_split_node_links_with_multiple_links(self):
        old_nodes = [TextNode("This is a text with a link [link text](https://example.com) and another [link text 2](https://example.com/2)", TextType.TEXT)]
        new_nodes = split_node_links(old_nodes)
        self.assertEqual(
            new_nodes, 
            [
                TextNode("This is a text with a link ", TextType.TEXT), 
                TextNode("link text", TextType.LINK, "https://example.com"), 
                TextNode(" and another ", TextType.TEXT), 
                TextNode("link text 2", TextType.LINK, "https://example.com/2"), 
            ]
        )
        
    def test_split_node_links_no_link(self):
        old_nodes = [TextNode("This is a text with no link", TextType.TEXT)]
        new_nodes = split_node_links(old_nodes)
        self.assertEqual(new_nodes, [TextNode("This is a text with no link", TextType.TEXT)])
