from pathlib import Path

# -------------------------------
# Directories to ignore in the tree
# -------------------------------
IGNORE = {".venv", "__pycache__", ".git"}


def print_tree(path: Path, prefix: str = "") -> None:
    """
    Recursively print a directory tree structure.

    Args:
        path (Path): The root directory to print.
        prefix (str): The prefix string used for indentation.
    """
    # Sort: directories first, then files (alphabetical)
    items = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    # Filter out ignored directories/files
    items = [p for p in items if p.name not in IGNORE]

    for i, item in enumerate(items):
        connector = "└── " if i == len(items) - 1 else "├── "
        print(prefix + connector + item.name)

        if item.is_dir():
            # Extend prefix for nested items
            extension = "    " if i == len(items) - 1 else "│   "
            print_tree(item, prefix + extension)


if __name__ == "__main__":
    print(".")
    print_tree(Path("."))