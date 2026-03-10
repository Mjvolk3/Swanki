"""Pre-commit hook to auto-fix dendron notes after Python file renames.

When a .py file is renamed/moved, this hook:
1. Detects the rename via git staging area
2. Moves ALL dendron notes under that prefix (note + children)
3. Updates wiki-links in all notes that referenced the old path

Replaces dendron-cli note move (which is currently broken).

Example: renaming ibiofoundry_ai/cli.py -> ibiofoundry_ai/app/cli.py
  auto-moves:
    notes/ibiofoundry_ai.cli.md              -> notes/ibiofoundry_ai.app.cli.md
    notes/ibiofoundry_ai.cli.plan.2026.md    -> notes/ibiofoundry_ai.app.cli.plan.2026.md
  auto-updates wiki-links in all notes/:
    [[ibiofoundry_ai.cli]]        -> [[ibiofoundry_ai.app.cli]]
    [[My CLI|ibiofoundry_ai.cli]] -> [[My CLI|ibiofoundry_ai.app.cli]]
"""
import re
import subprocess
import sys
from os.path import splitext
from pathlib import Path


def to_dendron_fname(file_path: str) -> str:
    """Convert a Python file path to a dendron fname."""
    path = file_path
    ext = splitext(path)[-1]
    if ext == ".py":
        path = path.removesuffix(".py")
    return path.replace("/", ".")


def get_renamed_py_files() -> list[tuple[str, str]]:
    """Detect renamed .py files in the git staging area."""
    result = subprocess.run(
        ["git", "diff", "--cached", "-M", "--diff-filter=R", "--name-status"],
        capture_output=True,
        text=True,
    )
    renames = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        # Format: R100\told_path\tnew_path
        parts = line.split("\t")
        if len(parts) >= 3 and parts[1].endswith(".py"):
            renames.append((parts[1], parts[2]))
    return renames


def find_orphaned_notes(old_path: str, new_path: str) -> list[tuple[Path, Path]]:
    """Find dendron notes that still use the old prefix after a file rename.

    Returns list of (current_note_path, expected_note_path) tuples.
    """
    old_fname = to_dendron_fname(old_path)
    new_fname = to_dendron_fname(new_path)
    notes_dir = Path("notes")

    orphaned = []

    # Check exact match: notes/ibiofoundry_ai.cli.md
    exact = notes_dir / f"{old_fname}.md"
    if exact.exists():
        target = notes_dir / f"{new_fname}.md"
        orphaned.append((exact, target))

    # Check children: notes/ibiofoundry_ai.cli.*.md
    # Dot-prefix avoids false positives (cli won't match client)
    for note in sorted(notes_dir.glob(f"{old_fname}.*.md")):
        old_note_fname = note.stem
        new_note_fname = new_fname + old_note_fname[len(old_fname) :]
        target = notes_dir / f"{new_note_fname}.md"
        orphaned.append((note, target))

    return orphaned


def move_notes(orphaned: list[tuple[Path, Path]]) -> None:
    """Rename note files from old path to new path."""
    for current, target in orphaned:
        target.parent.mkdir(parents=True, exist_ok=True)
        current.rename(target)
        print(f"  Moved: {current} -> {target}")


def update_wiki_links(fname_renames: list[tuple[str, str]]) -> list[Path]:
    """Update wiki-links across all notes that reference renamed fnames.

    Handles these wiki-link patterns:
      [[old.fname]]              -> [[new.fname]]
      [[old.fname#header]]       -> [[new.fname#header]]
      [[Display|old.fname]]      -> [[Display|new.fname]]
      [[Display|old.fname#hdr]]  -> [[Display|new.fname#hdr]]

    Returns list of modified note files.
    """
    notes_dir = Path("notes")
    all_notes = list(notes_dir.glob("**/*.md"))
    modified = []

    for note_path in all_notes:
        content = note_path.read_text()
        original = content

        for old_fname, new_fname in fname_renames:
            # Escape dots for regex
            old_escaped = re.escape(old_fname)

            # Pattern: [[...old.fname...]] — match old_fname at a word boundary
            # within wiki-links, preserving display text and anchors
            # Matches: [[old.fname]], [[old.fname#hdr]], [[Text|old.fname]], [[Text|old.fname#hdr]]
            # Also matches children: [[old.fname.child]], [[Text|old.fname.child#hdr]]
            pattern = rf"(\[\[(?:[^\]|]*\|)?)({old_escaped})((?:\.[^\]#]*)?(?:#[^\]]*)?\]\])"
            content = re.sub(pattern, rf"\1{new_fname}\3", content)

        if content != original:
            note_path.write_text(content)
            modified.append(note_path)

    return modified


def main():
    renames = get_renamed_py_files()
    if not renames:
        sys.exit(0)

    all_orphaned: list[tuple[str, str, list[tuple[Path, Path]]]] = []
    fname_renames: list[tuple[str, str]] = []

    for old_path, new_path in renames:
        orphaned = find_orphaned_notes(old_path, new_path)
        if orphaned:
            all_orphaned.append((old_path, new_path, orphaned))
            # Collect all old->new fname mappings (note + children)
            for current, target in orphaned:
                fname_renames.append((current.stem, target.stem))

    if not all_orphaned:
        sys.exit(0)

    # Auto-fix: move the note files
    print("Auto-moving dendron notes after Python file rename(s):\n")
    for old_path, new_path, orphaned in all_orphaned:
        print(f"  {old_path} -> {new_path}")
        move_notes(orphaned)

    # Auto-fix: update wiki-links in all notes
    modified = update_wiki_links(fname_renames)
    if modified:
        print(f"\nUpdated wiki-links in {len(modified)} note(s):")
        for f in modified:
            print(f"  {f}")

    # Tell the user to stage the changes
    print("\nDendron notes moved and wiki-links updated.")
    print("Please stage the changes and re-commit:")
    print("  git add notes/")
    sys.exit(1)


if __name__ == "__main__":
    main()
