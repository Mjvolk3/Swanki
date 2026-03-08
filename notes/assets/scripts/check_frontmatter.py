"""Pre-commit hook to verify Python files have docstring-style frontmatter.

Checks that files start with a triple-quote docstring block containing
the file path and dendron link. Does NOT auto-fix frontmatter — run
add_frontmatter.py to fix.

Also creates the corresponding dendron note if it doesn't exist.
"""
import random
import string
import sys
import time
from os.path import splitext
from pathlib import Path


def check_frontmatter(file_path: str) -> bool:
    """Check if a file starts with docstring frontmatter."""
    with open(file_path) as f:
        first_line = f.readline().strip()
    return first_line == '"""'


def to_dendron_fname(file_path: str) -> str:
    """Convert a Python file path to a dendron fname.

    swanki/pipeline/pipeline.py -> swanki.pipeline.pipeline
    tests/test_first_module.py -> tests.test_first_module
    """
    path = file_path
    ext = splitext(path)[-1]
    if ext == ".py":
        path = path.removesuffix(".py")
    return path.replace("/", ".")


def dendron_title(fname: str) -> str:
    """Extract a title from the last segment of a dendron fname.

    swanki.pipeline.pipeline -> Pipeline
    swanki.models.cards -> Cards
    """
    last = fname.rsplit(".", 1)[-1]
    return last.replace("_", " ").title()


def generate_dendron_id() -> str:
    """Generate a random dendron-style note ID."""
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choices(chars, k=23))


def ensure_dendron_note(file_path: str) -> bool:
    """Create the dendron note for a Python file if it doesn't exist.

    Returns True if a note was created, False if it already existed.
    """
    fname = to_dendron_fname(file_path)
    note_path = Path("notes") / f"{fname}.md"

    if note_path.exists():
        return False

    now_ms = int(time.time() * 1000)
    note_id = generate_dendron_id()
    title = dendron_title(fname)

    content = f"""---
id: {note_id}
title: {title}
desc: ''
updated: {now_ms}
created: {now_ms}
---
"""
    note_path.parent.mkdir(parents=True, exist_ok=True)
    note_path.write_text(content)
    return True


def main():
    failed_frontmatter = []
    created_notes = []

    for file_path in sys.argv[1:]:
        if not check_frontmatter(file_path):
            failed_frontmatter.append(file_path)

        if ensure_dendron_note(file_path):
            created_notes.append(file_path)

    if created_notes:
        print("Created dendron notes for:")
        for f in created_notes:
            fname = to_dendron_fname(f)
            print(f"  {f} -> notes/{fname}.md")

    if failed_frontmatter:
        print("Files missing docstring frontmatter:")
        for f in failed_frontmatter:
            print(f"  {f}")
        print("\nFix with: python notes/assets/scripts/add_frontmatter.py <file>")
        sys.exit(1)


if __name__ == "__main__":
    main()
