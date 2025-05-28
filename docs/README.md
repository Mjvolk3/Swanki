# Swanki Documentation

This directory contains the documentation for Swanki, built with Sphinx and hosted on Read the Docs.

## Building Documentation Locally

1. Install documentation dependencies:
   ```bash
   pip install -r docs/requirements.txt
   ```

2. Build the documentation:
   ```bash
   cd docs
   make clean
   make html
   ```

3. View the built documentation:
   ```bash
   open _build/html/index.html  # macOS
   # or
   python -m http.server -d _build/html 8000  # Then visit http://localhost:8000
   ```

## Documentation Structure

- `conf.py` - Sphinx configuration
- `index.rst` - Main documentation index
- `api/` - Auto-generated API documentation
- `*.md` - User guide pages (using MyST parser)
- `requirements.txt` - Documentation dependencies

## Read the Docs Setup

The documentation is configured for Read the Docs via `.readthedocs.yaml` in the project root.

## Writing Documentation

- Use NumPy-style docstrings in Python code
- User guide pages can be written in Markdown (`.md`) or reStructuredText (`.rst`)
- API documentation is auto-generated from docstrings