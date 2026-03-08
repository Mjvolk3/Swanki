"""
notes/assets/scripts/add_frontmatter
[[notes.assets.scripts.add_frontmatter]]
https://github.com/Mjvolk3/Swanki/tree/main/notes/assets/scripts/add_frontmatter
"""
import os
import os.path as osp
import sys
from dotenv import load_dotenv
load_dotenv()
from os.path import splitext
WORKSPACE_DIR = os.environ.get("WORKSPACE_DIR")
PYTHON_PKG_REL_PATH = os.environ.get("PYTHON_PKG_REL_PATH")
PYTHON_PKG_TEST_REL_PATH = os.environ.get("PYTHON_PKG_TEST_REL_PATH")
GIT_REPO_URL = os.environ.get("GIT_REPO_URL")

def add_frontmatter(file_path):
    # Extract the relative path
    print(f"file path:{file_path}")
    relative_path = osp.relpath(
        file_path, start=WORKSPACE_DIR
    )
    print(f"relative path:{relative_path}")

    # Detect whether input is a test file
    is_test_file = (
        PYTHON_PKG_TEST_REL_PATH
        and relative_path.startswith(PYTHON_PKG_TEST_REL_PATH)
    )

    # Generate the frontmatter lines
    # Assuming relative_path contains the file path
    file_extension = splitext(relative_path)[-1]

    # Strip known extensions for the dendron path
    stripped_path = relative_path
    if file_extension in (".py", ".sh"):
        stripped_path = relative_path[: -len(file_extension)]

    dendron_path = stripped_path.replace('/', '.')

    # Choose comment style based on file type
    use_hash = file_extension == ".sh"

    if use_hash:
        lines = [
            f"# {relative_path}\n",
            f"# [[{dendron_path}]]\n",
            f"# {GIT_REPO_URL}/tree/main/{relative_path}\n",
        ]
    else:
        lines = [
            f'"""\n',
            f"{relative_path}\n",
            f"[[{dendron_path}]]\n",
            f"{GIT_REPO_URL}/tree/main/{relative_path}\n",
        ]

    # Source files get a "Test file:" line; test files do not
    if not is_test_file and PYTHON_PKG_REL_PATH and PYTHON_PKG_TEST_REL_PATH:
        test_file_path = stripped_path.replace(PYTHON_PKG_REL_PATH, PYTHON_PKG_TEST_REL_PATH)
        test_file_path = osp.join(
            osp.dirname(test_file_path), "test_" + osp.basename(test_file_path)
        ) + file_extension
        prefix = "# " if use_hash else ""
        lines.append(f"{prefix}Test file: {test_file_path}\n")

    if not use_hash:
        lines.append(f'"""\n')

    with open(file_path, "r+") as file:
        content = file.readlines()

        print(
            f"Debug: First line of the file: {content[0] if content else 'File is empty'}"
        )

        # Check if frontmatter already exists (docstring or legacy comment style)
        if content and (content[0].strip() == '"""' or content[0].startswith("# " + relative_path)):
            print("Frontmatter already exists.")
            return

        # For shell files, preserve shebang at the top with a blank line separator
        if use_hash and content and content[0].startswith("#!"):
            shebang = content[0]
            content = [shebang, "\n"] + lines + ["\n"] + content[1:]
        else:
            content = lines + content

        file.seek(0)
        file.writelines(content)
        file.truncate()  # Ensure any leftover content is removed

    print("Frontmatter added successfully.")


if __name__ == "__main__":
    file_path = sys.argv[1]
    add_frontmatter(file_path)
