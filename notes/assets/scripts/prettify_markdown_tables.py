"""Pre-commit hook that aligns markdown table columns with padded pipes.

Only touches table blocks — all other content is left unchanged.

Usage:
    python notes/assets/scripts/prettify_markdown_tables.py [files...]
"""

import re
import sys


def is_table_row(line: str) -> bool:
    """Check if a line is a markdown table row (starts with |)."""
    return line.strip().startswith("|")


def is_separator_row(line: str) -> bool:
    """Check if a line is a table separator row (e.g., |---|---|)."""
    stripped = line.strip()
    if not stripped.startswith("|"):
        return False
    cells = [c.strip() for c in stripped.strip("|").split("|")]
    return all(re.match(r"^:?-+:?$", c) for c in cells if c)


def parse_table_row(line: str) -> list[str]:
    """Split a table row into cell contents."""
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [c.strip() for c in stripped.split("|")]


def format_separator_cell(original: str, width: int) -> str:
    """Format a separator cell preserving alignment markers."""
    original = original.strip()
    left = original.startswith(":")
    right = original.endswith(":")
    if left and right:
        return ":" + "-" * (width - 2) + ":"
    elif right:
        return "-" * (width - 1) + ":"
    elif left:
        return ":" + "-" * (width - 1)
    return "-" * width


def prettify_table(table_lines: list[str]) -> list[str]:
    """Align columns in a markdown table."""
    rows = [parse_table_row(line) for line in table_lines]
    num_cols = max(len(row) for row in rows)

    # Pad rows with fewer columns
    for row in rows:
        while len(row) < num_cols:
            row.append("")

    # Calculate max width per column
    col_widths = []
    for col in range(num_cols):
        max_w = 0
        for i, row in enumerate(rows):
            cell = row[col]
            if is_separator_row(table_lines[i]):
                max_w = max(max_w, 3)  # minimum separator width
            else:
                max_w = max(max_w, len(cell))
        col_widths.append(max_w)

    result = []
    for i, row in enumerate(rows):
        if is_separator_row(table_lines[i]):
            cells = []
            for col, cell in enumerate(row):
                w = col_widths[col] + 2  # +2 for the spaces around content cells
                cells.append(format_separator_cell(cell, w))
            result.append("|" + "|".join(cells) + "|")
        else:
            cells = []
            for col, cell in enumerate(row):
                cells.append(cell.ljust(col_widths[col]))
            result.append("| " + " | ".join(cells) + " |")
    return result


def prettify_file(filepath: str) -> bool:
    """Prettify tables in a file. Returns True if file was modified."""
    with open(filepath, encoding="utf-8") as f:
        lines = f.readlines()

    output = []
    table_block: list[str] = []
    modified = False

    def flush_table():
        nonlocal modified
        if table_block:
            prettified = prettify_table(table_block)
            for orig, new in zip(table_block, prettified):
                if orig.rstrip("\n") != new:
                    modified = True
            output.extend(line + "\n" for line in prettified)
            table_block.clear()

    for line in lines:
        stripped = line.rstrip("\n")
        if is_table_row(stripped):
            table_block.append(stripped)
        else:
            flush_table()
            output.append(line)

    flush_table()

    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(output)
    return modified


def main():
    if len(sys.argv) < 2:
        print("Usage: prettify_markdown_tables.py <file> [file...]")
        sys.exit(1)

    exit_code = 0
    for filepath in sys.argv[1:]:
        if prettify_file(filepath):
            print(f"Prettified tables in {filepath}")
            exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
