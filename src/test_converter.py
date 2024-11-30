
import unittest
from converter import block_to_block_type, extract_title, markdown_to_blocks, markdown_to_html_node, split_node_images, split_node_links, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, text_to_nodes
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
    
    def test_split_nodes_delimiter_italic(self):
        old_nodes = [TextNode("This is a text node with a *italic* text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        self.assertEqual(
            new_nodes, 
            [
                TextNode("This is a text node with a ", TextType.TEXT), 
                TextNode("italic", TextType.ITALIC), 
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
    
    def test_text_to_nodes(self):
        text =  """This is a text with a link [link text](https://example.com) and an image ![alt text](https://example.com),
            and a **bold** text, also you can see *italic* text, and finally a `code` text."""
        
        nodes = text_to_nodes(text)
        assert nodes == [
            TextNode("This is a text with a link ", TextType.TEXT), 
            TextNode("link text", TextType.LINK, "https://example.com"), 
            TextNode(" and an image ", TextType.TEXT), 
            TextNode("alt text", TextType.IMAGE, "https://example.com"), 
            TextNode(",\n            and a ", TextType.TEXT), 
            TextNode("bold", TextType.BOLD), 
            TextNode(" text, also you can see ", TextType.TEXT), 
            TextNode("italic", TextType.ITALIC), 
            TextNode(" text, and finally a ", TextType.TEXT), 
            TextNode("code", TextType.CODE), 
            TextNode(" text.", TextType.TEXT)
        ]

    def test_text_to_nodes_only_text(self):
        text = "This is a text"
        nodes = text_to_nodes(text)
        assert nodes == [TextNode("This is a text", TextType.TEXT)]
    
    def test_text_to_nodes_only_bold(self):
        text = "**This is a bold text**"
        nodes = text_to_nodes(text)
        assert nodes == [TextNode("This is a bold text", TextType.BOLD)]
    
    def test_text_to_nodes_empty_text(self):
        text = ""
        nodes = text_to_nodes(text)
        assert nodes == [TextNode("", TextType.TEXT)]

    def test_markdown_to_blocks(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""

        texts = markdown_to_blocks(markdown)
        assert texts == [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]

    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("# This is a heading"), "heading")
        self.assertEqual(block_to_block_type("```This is a codeblock```"), "codeblock")
        self.assertEqual(block_to_block_type("> This is a quote"), "quote")
        self.assertEqual(block_to_block_type("- This is an unordered list"), "unordered_list")
        self.assertEqual(block_to_block_type("1. This is an ordered list"), "ordered_list")
        self.assertEqual(block_to_block_type("This is a paragraph"), "paragraph")

    def test_markdown_to_html_node(self):
        markdown = """# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it."""
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(html_node.props, {})
        self.assertEqual(len(html_node.children), 2)
        self.assertEqual(html_node.children[0].tag, "h1")
        self.assertEqual(html_node.children[1].tag, "p")    

    def test_markdown_to_html_node_code_and_blockquote(self):
        markdown = """```This is a codeblock```\n\n> This is a quote"""
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(html_node.props, {})
        self.assertEqual(len(html_node.children), 2)
        self.assertEqual(html_node.children[0].tag, "pre")
        self.assertEqual(html_node.children[1].tag, "blockquote")

    def test_markdown_to_html_node_unordered_list(self):
        markdown = """- This is the first list item in a list block\n- This is a list item\n- This is another list item"""
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(html_node.props, {})
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].tag, "ul")

    def test_markdown_to_html_node_ordered_list(self):
        markdown = """1. This is the first list item in a list block\n2. This is a list item\n3. This is another list item"""
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(html_node.props, {})
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].tag, "ol")
    
    def test_extract_title(self):
        markdown = """# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it."""
        title = extract_title(markdown)
        self.assertEqual(title, "This is a heading")