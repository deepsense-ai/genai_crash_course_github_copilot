## Dependency management

This repository uses `uv` to manage Python dependencies.
- `uv sync` to install dependencies from `uv.lock`
- `uv add <package>` to add a new dependency and update `uv.lock`
- `uv remove <package>` to remove a dependency and update `uv.lock`
- `uv run <command>` to run a command in the virtual environment

Always use `uv` to manage dependencies and run python scripts.

## Code formatting

Repository uses a short, concise Google-style docstring formatting.
Docstrings are applicable to functions, classes, and methods. No module-level docstrings.
