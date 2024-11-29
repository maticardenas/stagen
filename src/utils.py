from pathlib import Path
import shutil
import re


def is_markdown_heading(text: str) -> bool:
    """Headings start with 1-6 # characters, 
    followed by a space and then the heading text."""
    
    return bool(re.match(r"^#{1,6} .*$", text))

def is_markdown_codeblock(text: str) -> bool:
    """Code blocks start with 3 backticks and end with 3 backticks, 
    including break lines in the middle, and including tabulations"""

    return bool(re.match(r"```(\n*.*\n*)```$", text))

def is_markdown_ordered_list(text: str) -> bool:
    """Every line in an ordered list block must start with a number 
    followed by a . character and a space. The number must start at 1 and increment by 1 for each line."""
    
    last_number = 0

    for line in text.split("\n"):
        if not re.match(r"^\d+\. .*$", line):
            return False

        try:
            number = int(line.split(".")[0])
        except ValueError:
            print("Error: The first character of the line is not a number")

        if number == last_number + 1:
            last_number = number
        else:
            print("The ordered list is not sequential")
            return False
    
    return True

def remove_everything_dir(dir: Path) -> None:
    """ Removes everything in a directory, including all its subdirectories and files """
    for item in dir.iterdir():
        if item.is_dir():
            remove_everything_dir(item)
        else:
            item.unlink()

def copy_dir_content(src: Path, dest: Path) -> None:
    """ Copies a directory content, including all its subdirectories and files, to another directory """ 
    dest.mkdir(exist_ok=True)
    # remove everything in the destination directory
    remove_everything_dir(dest)

    for item in src.iterdir():
        if item.is_dir():
            copy_dir_content(item, dest / item.name)
        else:
            item_dest = dest / item.name
            shutil.copy(item, item_dest)