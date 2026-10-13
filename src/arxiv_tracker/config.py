"""Load tracker settings from a TOML file."""

import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    """Settings for the arXiv search."""

    keywords: list[str]
    max_results: int = 50


def load_config(path: Path) -> Config:
    """Read the [search] section of a TOML config file."""
    with path.open("rb") as file:
        data = tomllib.load(file)
    search = data["search"]
    return Config(
        keywords=search["keywords"],
        max_results=search.get("max_results", 50),
    )
