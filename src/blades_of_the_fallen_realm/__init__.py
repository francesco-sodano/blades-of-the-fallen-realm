"""Blades of the Fallen Realm — A retro beat 'em up inspired by SEGA Golden Axe."""

import tomllib
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path


def _read_version_from_pyproject() -> str:
    """Read the project version from pyproject.toml when metadata is unavailable."""
    pyproject_path = Path(__file__).resolve().parents[2] / "pyproject.toml"
    with pyproject_path.open("rb") as pyproject_file:
        pyproject_data = tomllib.load(pyproject_file)
    return str(pyproject_data["project"]["version"])


try:
    # Docs: https://docs.python.org/3/library/importlib.metadata.html
    __version__ = version("blades_of_the_fallen_realm")
except PackageNotFoundError:
    __version__ = _read_version_from_pyproject()
