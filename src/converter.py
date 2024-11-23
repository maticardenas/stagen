
from src.htmlnode import HTMLNode, LeafNode
from src.textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    leaf_node_action = {
        TextType.TEXT.value: LeafNode(None, text_node.text),
        TextType.BOLD.value: LeafNode("b", text_node.text),
        TextType.ITALIC.value: LeafNode("i", text_node.text),
        TextType.LINK.value: LeafNode(tag="a", value=text_node.text, props={"href": text_node.url}),
        TextType.IMAGE.value: LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text}),
        TextType.CODE.value: LeafNode("code", text_node.text),
    }

    return leaf_node_action[text_node.text_type.value]