"""Load tracker settings from a TOML file."""

import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    """Settings for the arXiv search and the published site."""

    keywords: list[str]
    max_results: int = 50
    site_url: str = ""


def load_config(path: Path) -> Config:
    """Read the [search] and optional [site] sections of a TOML config file."""
    with path.open("rb") as file:
        data = tomllib.load(file)
    search = data["search"]
    site = data.get("site", {})
    return Config(
        keywords=search["keywords"],
        max_results=search.get("max_results", 50),
        site_url=site.get("url", ""),
    )
