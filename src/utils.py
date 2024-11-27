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