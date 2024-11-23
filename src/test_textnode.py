import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(str(node), "TextNode(This is a text node, 2, None)")

    def test_repr_with_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.google.com")
        self.assertEqual(str(node), "TextNode(This is a text node, 5, https://www.google.com)")


if __name__ == "__main__":
    unittest.main()