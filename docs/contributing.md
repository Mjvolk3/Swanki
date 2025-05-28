# Contributing to Swanki

We welcome contributions to Swanki! This document provides guidelines for contributing to the project.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/swanki.git
   cd swanki
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

## Code Style

- Follow PEP 8
- Use NumPy-style docstrings
- Add type hints to all functions
- Maximum line length: 88 characters (Black default)

## Testing

Run tests before submitting:

```bash
pytest tests/
```

## Documentation

- Update docstrings for any API changes
- Update user documentation if adding features
- Build docs locally to verify:
  ```bash
  cd docs
  make html
  ```

## Pull Request Process

1. Create a feature branch
2. Make your changes
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

## Reporting Issues

Use GitHub Issues to report bugs or request features. Include:
- Python version
- Swanki version
- Minimal reproducible example
- Error messages/logs