# Setup Guide: Installing Dependencies with uv

This guide walks you through the complete process of installing all dependencies for the Blades of the Fallen Realm project using `uv`, the fast Python package manager.

## Prerequisites

- Git (to clone the repository)
- Internet connection

## Step 1: Install uv

If you don't have `uv` installed, you can install it using one of these methods:

### Option A: Using the official installer (recommended)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Option B: Using pip
```bash
pip install uv
```

### Option C: Using pipx
```bash
pipx install uv
```

### Verify installation
```bash
uv --version
```

## Step 2: Clone the Repository (if not already done)

```bash
git clone https://github.com/francesco-sodano/blades-of-the-fallen-realm.git
cd blades-of-the-fallen-realm
```

## Step 3: Install Python 3.12.12

The project requires Python 3.12.12 specifically. Use `uv` to install it:

```bash
uv python install 3.12.12
```

This command downloads and installs the exact Python version needed.

## Step 4: Create Virtual Environment

Create a virtual environment using the correct Python version:

```bash
uv venv --python 3.12.12 .venv
```

This creates a `.venv` directory in your project root.

## Step 5: Install All Dependencies

Install both runtime and development dependencies in one command:

```bash
uv sync --group dev
```

This command:
- Reads `pyproject.toml` for all dependency specifications
- Installs runtime dependencies (pygame-ce)
- Installs dev dependencies (black, mypy, pytest, pytest-cov)
- Creates/updates `uv.lock` for reproducible builds
- Installs the project itself in editable mode

### What gets installed:

**Runtime Dependencies:**
- `pygame-ce>=2.5.3` - The game engine

**Development Dependencies:**
- `black==26.1.0` - Code formatter
- `mypy==1.19.1` - Static type checker
- `pytest==9.0.2` - Testing framework
- `pytest-cov==7.0.0` - Code coverage plugin

## Step 6: Verify Installation

Check that everything was installed correctly:

```bash
uv pip list
```

You should see all 18 packages listed, including:
- blades-of-the-fallen-realm (0.1.0)
- pygame-ce (2.5.6)
- black (26.1.0)
- mypy (1.19.1)
- pytest (9.0.2)
- pytest-cov (7.0.0)
- And their dependencies

## Step 7: Run Tests

Verify the installation works by running the test suite:

```bash
uv run python -m pytest tests/ -v
```

All tests should pass, confirming that:
- Python is correctly installed
- All dependencies are available
- The project environment is properly configured

## Quick Reference Commands

### Running the game
```bash
uv run python -m blades_of_the_fallen_realm
```

### Running tests
```bash
uv run pytest
```

### Running tests with coverage
```bash
uv run python -m pytest tests/ --cov=blades_of_the_fallen_realm --cov-report=term-missing
```

### Formatting code
```bash
uv run black .
```

### Type checking
```bash
uv run mypy src/
```

### Adding new dependencies

**Runtime dependency:**
```bash
uv add package-name
```

**Development dependency:**
```bash
uv add --group dev package-name
```

### Updating dependencies
```bash
uv sync --upgrade
```

## Troubleshooting

### Issue: "uv: command not found"
**Solution:** Make sure `uv` is installed and in your PATH. After installation, you may need to restart your terminal or run:
```bash
source ~/.bashrc  # or ~/.zshrc depending on your shell
```

### Issue: Python version mismatch
**Solution:** Ensure you're using Python 3.12.12:
```bash
uv python install 3.12.12
uv venv --python 3.12.12 .venv --force
uv sync --group dev
```

### Issue: Dependencies not found when running scripts
**Solution:** Use `uv run` prefix to ensure the virtual environment is active:
```bash
uv run python -m blades_of_the_fallen_realm
```

### Issue: Lock file out of sync
**Solution:** Regenerate the lock file:
```bash
uv lock
uv sync --group dev
```

## Using Dev Containers (Alternative Setup)

If you're using VS Code with Dev Containers:

1. Open the repository in VS Code
2. Click "Reopen in Container" when prompted
3. The container automatically runs `.devcontainer/scripts/postCreate.sh`, which:
   - Installs uv
   - Installs Python 3.12.12
   - Creates the virtual environment
   - Syncs all dependencies
   - Activates the venv for all terminal sessions

No manual steps needed!

## Summary

The complete one-line setup (after uv is installed):

```bash
uv python install 3.12.12 && uv venv --python 3.12.12 .venv && uv sync --group dev
```

That's it! You now have a fully configured development environment with all dependencies installed and ready to use.
