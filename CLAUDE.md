## Dendron Paths

Example:
[[Paper|Paper]] exists here `/Swanki/notes/Paper.md`

Example

![](./assets/images/fix_cloze.md.issue-with-cloze-card-no-data-in-extra.png) exists here `Swanki/notes/assets/images/fix_cloze.md.issue-with-cloze-card-no-data-in-extra.png`

## Coding Advice

- Don't be superfluous
- Don't use try except blocks - fail fast minimize other types of exception coding like by using excessive conditionals

## Python File Format

Every `.py` file starts with a single frontmatter docstring. The module description (if any) goes in the same block -- never a separate docstring.

```python
"""
swanki/audio/card.py
[[swanki.audio.card]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/audio/card.py
Test file: tests/test_audio_card.py

Flashcard audio generation with cloze handling and citation prefixing.
"""
```

Use **Google-style docstrings** for functions and classes (`Args:`, `Returns:`, `Raises:`). Ruff enforces `convention = "google"`. Keep docstrings concise -- no verbose parameter descriptions that duplicate type annotations. Pydantic models use `Field(description="...")` instead of docstrings for fields.

## Pydantic Models

- We want to use pydantic models to structure output as much as possible as opposed to controlling output by changing prompts.

## Files

- Tests should go in `tests/`

## Code Execution

- ~/opt/miniconda3/envs/swanki/bin/Swanki python script.py

## Weekly Notes

- When checking off a task in the weekly note, always add a one-sentence summary before the `[[link]]`. Never leave a checked item as just a bare link.

## Change Log

- This is automatically updated. Don't edit it directly.
