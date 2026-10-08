"""Fetch recent papers from the arXiv API."""

from dataclasses import dataclass
from urllib.parse import urlencode

import feedparser
import requests

ARXIV_API_URL = "https://export.arxiv.org/api/query"


@dataclass
class Paper:
    """A single arXiv paper."""

    arxiv_id: str
    title: str
    summary: str
    authors: list[str]
    published: str
    url: str


def _clean(text: str) -> str:
    """Collapse newlines and repeated spaces into single spaces."""
    return " ".join(text.split())


def build_query_url(keywords: list[str], max_results: int = 50) -> str:
    """Build an arXiv API URL that searches for any of the keywords."""
    search_query = " OR ".join(f'all:"{keyword}"' for keyword in keywords)
    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    return f"{ARXIV_API_URL}?{urlencode(params)}"


def parse_feed(xml_text: str) -> list[Paper]:
    """Turn an arXiv Atom feed into a list of Paper objects."""
    feed = feedparser.parse(xml_text)
    papers = []
    for entry in feed.entries:
        papers.append(
            Paper(
                arxiv_id=entry.id.rsplit("/", 1)[-1],
                title=_clean(entry.title),
                summary=_clean(entry.summary),
                authors=[author.name for author in entry.authors],
                published=entry.published,
                url=entry.link,
            )
        )
    return papers


def fetch_papers(keywords: list[str], max_results: int = 50) -> list[Paper]:
    """Download and parse the latest papers matching the keywords."""
    response = requests.get(build_query_url(keywords, max_results), timeout=30)
    response.raise_for_status()
    return parse_feed(response.text)
