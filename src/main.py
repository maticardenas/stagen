from pathlib import Path
from converter import generate_pages_recursively
from utils import copy_dir_content

CURRENT_PATH = Path(__file__).parent

def main():
    copy_dir_content(CURRENT_PATH.parent / "static", CURRENT_PATH.parent / "public")
    template_path = CURRENT_PATH.parent / "templates" / "template.html"
    generate_pages_recursively(
        dir_path_content=CURRENT_PATH.parent / "content", 
        template_path=template_path, 
        dest_dir_path=CURRENT_PATH.parent / "public"
    )

if __name__ == "__main__":
    main()