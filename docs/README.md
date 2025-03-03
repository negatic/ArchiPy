# ArchiPy Documentation

This directory contains the MkDocs-based documentation for ArchiPy.

## Documentation Structure

- `mkdocs.yml` - Main configuration file for MkDocs
- `docs/` - Markdown documentation files
  - `index.md` - Home page
  - `api_reference/` - API documentation
  - `examples/` - Usage examples
  - `assets/` - Images and other static assets

## Converting from Sphinx to MkDocs

The documentation is being migrated from Sphinx (RST) to MkDocs (Markdown). To help with this process:

1. Run the conversion script:
   ```bash
   python scripts/convert_docs.py
   ```
   This script uses `pandoc` to convert RST files to Markdown.

2. Manually review and improve the converted files.

3. Preview the documentation:
   ```bash
   make docs-serve
   ```

4. Build the documentation:
   ```bash
   make docs-build
   ```

5. Deploy to GitHub Pages:
   ```bash
   make docs-deploy
   ```

## Writing Documentation Guidelines

- Use Markdown syntax for all documentation files
- Follow the Google Python style for code examples
- Include type hints in code samples
- Group related documentation in directories
- Link between documentation pages using relative links
- Add admonitions (notes, warnings, tips) using the Material for MkDocs syntax:
  ```markdown
  !!! note
      This is a note.
  ```

## Improving Documentation

When improving the documentation:

1. Focus on clarity and conciseness
2. Include practical, runnable examples
3. Explain "why" not just "how"
4. Keep navigation logical and intuitive
5. Use diagrams for complex concepts