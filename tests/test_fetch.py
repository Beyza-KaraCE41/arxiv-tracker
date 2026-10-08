from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest
import requests

from arxiv_tracker.fetch import build_query_url, fetch_papers, parse_feed

FIXTURE = Path(__file__).parent / "fixtures" / "arxiv_sample.xml"


def load_sample() -> str:
    return FIXTURE.read_text(encoding="utf-8")


# --- build_query_url -------------------------------------------------------


def test_build_query_url_joins_keywords_with_or():
    url = build_query_url(["metal-organic framework", "linker"], max_results=10)
    params = parse_qs(urlparse(url).query)

    assert params["search_query"] == ['all:"metal-organic framework" OR all:"linker"']
    assert params["max_results"] == ["10"]
    assert params["sortBy"] == ["submittedDate"]


# --- parse_feed ------------------------------------------------------------


def test_parse_feed_returns_one_paper_per_entry():
    papers = parse_feed(load_sample())
    assert len(papers) == 2


def test_parse_feed_extracts_fields():
    paper = parse_feed(load_sample())[0]

    assert paper.arxiv_id == "2610.08536v1"
    assert paper.url == "https://arxiv.org/abs/2610.08536v1"
    assert paper.published == "2026-10-06T15:26:30Z"
    assert paper.authors == ["Hao Chen", "Tongyang Zhao"]


def test_parse_feed_cleans_whitespace_in_title():
    paper = parse_feed(load_sample())[0]
    expected = "Programming electronic states in conductive metal-organic frameworks"
    assert paper.title == expected


def test_parse_feed_keeps_non_ascii_author_names():
    paper = parse_feed(load_sample())[1]
    assert paper.authors == ["José Antonio Real", "Samuel Mañas-Valero"]


def test_parse_feed_handles_empty_feed():
    empty = '<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom"></feed>'
    assert parse_feed(empty) == []


# --- fetch_papers (network mocked) -----------------------------------------


class FakeResponse:
    def __init__(self, text: str):
        self.text = text

    def raise_for_status(self) -> None:
        pass


def test_fetch_papers_uses_http_response(monkeypatch):
    calls = []

    def fake_get(url, timeout):
        calls.append((url, timeout))
        return FakeResponse(load_sample())

    monkeypatch.setattr("arxiv_tracker.fetch.requests.get", fake_get)

    papers = fetch_papers(["metal-organic framework"], max_results=2)

    assert len(papers) == 2
    assert "max_results=2" in calls[0][0]
    assert calls[0][1] == 30


def test_fetch_papers_raises_on_http_error(monkeypatch):
    class ErrorResponse:
        def raise_for_status(self) -> None:
            raise requests.HTTPError("503 Service Unavailable")

    monkeypatch.setattr(
        "arxiv_tracker.fetch.requests.get", lambda url, timeout: ErrorResponse()
    )

    with pytest.raises(requests.HTTPError):
        fetch_papers(["anything"])
