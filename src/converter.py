
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


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type.value != TextType.TEXT.value:
            new_nodes.append(node)
            continue
                       
        if node.text.count(delimiter) > 1:
            split_text = node.text.split(delimiter)
            for i, text in enumerate(split_text):
                if i % 2 == 0:
                    new_nodes.append(TextNode(text, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(text, text_type))
        elif node.text.count(delimiter) == 1:
            raise Exception("delimiter should have a matching closing one.")
        else:
            print("No delimiter found, returning the same node.")
            return old_nodes
    return new_nodes