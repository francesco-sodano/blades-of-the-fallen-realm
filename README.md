# Blades Of The Fallen Realm

Blades Of The Fallen Realm.

## Features

- Feature 1
- Feature 2
- Feature 3

## Requirements

- Python 3.12

## Installation

```bash
git clone https://github.com/francesco-sodano/blades-of-the-fallen-realm.git
cd blades-of-the-fallen-realm
uv sync --group dev
```

## Usage

```bash
python -m blades_of_the_fallen_realm
```

## Development

This project uses [uv](https://docs.astral.sh/uv/) as the package manager and a [Dev Container](https://containers.dev/) for a consistent development environment.

### Quick start

1. Open the repo in VS Code and select **"Reopen in Container"**.
2. The dev container installs Python 3.12, creates a `.venv`, and syncs all dependencies automatically.

### Project structure

```
src/blades_of_the_fallen_realm/   # Package source code
tests/                            # Tests (pytest)
scripts/                          # Helper scripts
```

### Run tests

```bash
pytest
```

### Format & lint

```bash
black .
mypy src/
```

## Docker

```bash
docker build -t blades_of_the_fallen_realm .
docker run --rm blades_of_the_fallen_realm
```

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.