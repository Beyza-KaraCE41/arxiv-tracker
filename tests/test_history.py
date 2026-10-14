import json

import requests

from arxiv_tracker.fetch import Paper
from arxiv_tracker.history import find_new_ids, load_previous_ids, save_ids

URL = "https://example.com/papers.json"


def make_paper(arxiv_id: str) -> Paper:
    return Paper(
        arxiv_id=arxiv_id,
        title="MOF study",
        summary="",
        authors=[],
        published="2026-10-01T00:00:00Z",
        url=f"https://arxiv.org/abs/{arxiv_id}",
    )


class FakeResponse:
    def __init__(self, data):
        self._data = data

    def raise_for_status(self) -> None:
        pass

    def json(self):
        return self._data


class NotFoundResponse:
    def raise_for_status(self) -> None:
        raise requests.HTTPError("404 Not Found")


# --- find_new_ids ----------------------------------------------------------


def test_find_new_ids_returns_papers_not_seen_before():
    papers = [make_paper("1"), make_paper("2"), make_paper("3")]
    assert find_new_ids(papers, {"1", "2"}) == {"3"}


def test_find_new_ids_marks_nothing_on_first_run():
    papers = [make_paper("1"), make_paper("2")]
    assert find_new_ids(papers, None) == set()


# --- save_ids --------------------------------------------------------------


def test_save_ids_writes_a_json_list(tmp_path):
    path = tmp_path / "papers.json"
    save_ids([make_paper("1"), make_paper("2")], path)
    assert json.loads(path.read_text(encoding="utf-8")) == ["1", "2"]


# --- load_previous_ids -----------------------------------------------------


def test_load_previous_ids_reads_json(monkeypatch):
    monkeypatch.setattr(
        "arxiv_tracker.history.requests.get",
        lambda url, timeout: FakeResponse(["1", "2"]),
    )
    assert load_previous_ids(URL) == {"1", "2"}


def test_load_previous_ids_returns_none_when_file_is_missing(monkeypatch):
    monkeypatch.setattr(
        "arxiv_tracker.history.requests.get",
        lambda url, timeout: NotFoundResponse(),
    )
    assert load_previous_ids(URL) is None


def test_load_previous_ids_returns_none_when_network_fails(monkeypatch):
    def failing_get(url, timeout):
        raise requests.ConnectionError("no network")

    monkeypatch.setattr("arxiv_tracker.history.requests.get", failing_get)
    assert load_previous_ids(URL) is None
