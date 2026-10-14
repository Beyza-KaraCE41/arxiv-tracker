"""Remember which papers were shown on the previous run."""

import json
from pathlib import Path

import requests

from arxiv_tracker.fetch import Paper


def load_previous_ids(url: str) -> set[str] | None:
    """Download the paper IDs published by the previous run.

    Returns None when they cannot be loaded (first run, missing file,
    network error), so the site can still be built without "new" badges.
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return set(response.json())
    except (requests.RequestException, ValueError):
        return None


def save_ids(papers: list[Paper], path: Path) -> None:
    """Save the IDs of the given papers as a JSON list."""
    ids = [paper.arxiv_id for paper in papers]
    path.write_text(json.dumps(ids, indent=2), encoding="utf-8")


def find_new_ids(papers: list[Paper], previous_ids: set[str] | None) -> set[str]:
    """Return IDs of papers that were not shown on the previous run.

    On the first run (no previous data) nothing is marked as new.
    """
    if previous_ids is None:
        return set()
    return {paper.arxiv_id for paper in papers if paper.arxiv_id not in previous_ids}
