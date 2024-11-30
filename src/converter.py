
from pathlib import Path
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
import re

from utils import is_markdown_codeblock, is_markdown_heading, is_markdown_ordered_list


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    leaf_node_action = {
        TextType.TEXT.value: LeafNode(None, value=text_node.text),
        TextType.BOLD.value: LeafNode("b", value=text_node.text),
        TextType.ITALIC.value: LeafNode("i", value=text_node.text),
        TextType.LINK.value: LeafNode(tag="a", value=text_node.text, props={"href": text_node.url}),
        TextType.IMAGE.value: LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text}),
        TextType.CODE.value: LeafNode("code", value=text_node.text),
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
                if text != "":
                    if i % 2 == 0:
                        new_nodes.append(TextNode(text, TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(text, text_type))
        elif node.text.count(delimiter) == 1:
            raise Exception("delimiter should have a matching closing one.")
        else:
            print("No delimiter found, adding the same node.")
            new_nodes.append(node)
        
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


def split_node_links(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type.value != TextType.TEXT.value:
            new_nodes.append(node)
            continue
        
        split_by_link = re.split(r"\[([^\]]*)\]\(([^)]*)\)", node.text)

        if len(split_by_link) == 1:
            print("No link found, returning the same node.")
            new_nodes.append(node)
        else:
            for i, text in enumerate(split_by_link):
                if i % 3 == 0 and text != "":
                    new_nodes.append(TextNode(text, TextType.TEXT))
                elif i % 3 == 1:
                    new_nodes.append(TextNode(text, TextType.LINK, split_by_link[i + 1]))
                else:
                    continue

    return new_nodes

def text_to_nodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_node_images(nodes)
        
    nodes = split_node_links(nodes)



    return nodes


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


def block_to_block_type(block: str) -> str:
    if is_markdown_heading(block):
        return "heading"
    elif is_markdown_codeblock(block):
        return "codeblock"
    elif block.startswith(">"):
        return "quote"
    elif block.startswith("- ") or block.startswith("* "):
        return "unordered_list" 
    elif is_markdown_ordered_list(block):
        return "ordered_list"
    else:
        return "paragraph"


def markdown_to_blocks(markdown: str) -> list[str]:
    split_markdown = markdown.split("\n\n")
    return [markdown_block.strip() for markdown_block in split_markdown]


def text_to_children(text: str) -> list[HTMLNode]:
    nodes = text_to_nodes(text)
    children = [text_node_to_html_node(node) for node in nodes]
    return children


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == "heading":
            heading_length = len(block.split(" ")[0])
            node = ParentNode(f"h{heading_length}", block[heading_length + 1:])
            children = text_to_children(block[heading_length + 1:])
            node.children = children
            html_nodes.append(node)
        elif block_type == "codeblock":
            node = LeafNode("pre", f"<code>{block[3:-3]}</code>")
            html_nodes.append(node)
        elif block_type == "quote":
            block_text = block.split("> ")[1]
            node = ParentNode(f"blockquote", block_text)
            children = text_to_children(block_text)
            node.children = children
            html_nodes.append(node)
        elif block_type == "unordered_list":
            all_children = []
            for item in block.split("\n"):
                children = text_to_children(item[2:])
                all_children.append(ParentNode("li", children))            
            node = ParentNode("ul", all_children)
            html_nodes.append(node)
        elif block_type == "ordered_list":
            all_children = []
            for item in block.split("\n"):
                children = text_to_children(item[3:])
                all_children.append(ParentNode("li", children))
            node = ParentNode(tag="ol", children=all_children)
            html_nodes.append(node)
        elif block_type == "paragraph":
            node = ParentNode("p", block)
            children = text_to_children(block)
            node.children = children
            html_nodes.append(node)

    return ParentNode("div", html_nodes)

def extract_title(markdown: str) -> str:
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if is_markdown_heading(block):
            return block.split("# ")[1]

    raise Exception("No title found in the markdown")


def generate_page(from_path: Path, template_path: Path, dest_path: Path) -> None:
    print(f"Generating page from {from_path} to {dest_path}, using template {template_path}")
    
    markdown = from_path.read_text()
    template = template_path.read_text()

    title = extract_title(markdown)
    html_node = markdown_to_html_node(markdown)
    html_text = html_node.to_html()
    
    replaced_template_text = template.replace("{{ Title }}", title).replace("{{ Content }}", html_text)

    dest_path.write_text(replaced_template_text)


def generate_pages_recursively(dir_path_content: Path, template_path: Path, dest_dir_path: Path) -> None:
    for item in dir_path_content.iterdir():
        if item.is_dir():
            dest_dir_sub_dir = dest_dir_path / item.name
            dest_dir_sub_dir.mkdir(exist_ok=True)
            generate_pages_recursively(
                dir_path_content=item, 
                template_path=template_path, 
                dest_dir_path=dest_dir_sub_dir
            )
        else:
            if item.suffix == ".md":
                dest_path = dest_dir_path / item.name.replace(".md", ".html")
                generate_page(
                    from_path=item, 
                    template_path=template_path, 
                    dest_path=dest_path
                )