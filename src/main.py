from pathlib import Path
from utils import copy_dir_content

CURRENT_PATH = Path(__file__).parent

def main():
    copy_dir_content(CURRENT_PATH.parent / "static", CURRENT_PATH.parent / "public")


if __name__ == "__main__":
    main()