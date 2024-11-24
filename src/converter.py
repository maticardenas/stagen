
from src.htmlnode import HTMLNode, LeafNode
from src.textnode import TextNode, TextType
import re


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

def split_node_images(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type.value != TextType.TEXT.value:
            new_nodes.append(node)
            continue
        
        split_by_image = re.split(r"!\[([^\]]*)\]\(([^)]*)\)", node.text)

        if len(split_by_image) == 1:
            print("No image found, returning the same node.")
            new_nodes.append(node)
        else:
            for i, text in enumerate(split_by_image):
                if i % 3 == 0 and text != "":
                    new_nodes.append(TextNode(text, TextType.TEXT))
                elif i % 3 == 1:
                    new_nodes.append(TextNode(text, TextType.IMAGE, split_by_image[i + 1]))
                else:
                    continue

    return new_nodes


def split_by_image(text: str) -> list[str]:
    return re.split(r"!\[([^\]]*)\]\(([^)]*)\)", text)


def extract_markdown_images(text: str) -> list[tuple]:
    images = []
    for match in re.finditer(r"!\[([^\]]*)\]\(([^)]*)\)", text):
        images.append((match.group(1), match.group(2)))
    
    return images   


def extract_markdown_links(text: str) -> list[tuple]:
    links = []
    for match in re.finditer(r"\[([^\]]*)\]\(([^)]*)\)", text):
        links.append((match.group(1), match.group(2)))
    
    return links
