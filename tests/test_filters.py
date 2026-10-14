from arxiv_tracker.fetch import Paper
from arxiv_tracker.filters import filter_papers, matches_keywords


def make_paper(
    arxiv_id: str,
    title: str,
    summary: str = "",
    published: str = "2026-10-01T00:00:00Z",
) -> Paper:
    return Paper(
        arxiv_id=arxiv_id,
        title=title,
        summary=summary,
        authors=[],
        published=published,
        url=f"https://arxiv.org/abs/{arxiv_id}",
    )


# --- matches_keywords ------------------------------------------------------


def test_matches_when_keyword_present():
    text = "A new metal-organic framework for CO2 capture"
    assert matches_keywords(text, ["metal-organic framework"])


def test_is_case_insensitive():
    text = "Metal-Organic Framework Design"
    assert matches_keywords(text, ["metal-organic framework"])


def test_returns_false_when_no_keyword_matches():
    text = "Introduction to quantum computing"
    assert not matches_keywords(text, ["metal-organic framework"])


def test_returns_false_for_empty_keyword_list():
    assert not matches_keywords("Any text", [])


def test_matches_when_hyphen_is_written_as_space():
    text = "A new metal organic framework for CO2 capture"
    assert matches_keywords(text, ["metal-organic framework"])


def test_matches_when_words_are_not_adjacent():
    text = "Organic linkers used in MOFs"
    assert matches_keywords(text, ["MOF linker"])


def test_matches_across_line_breaks():
    text = "Conductive metal-organic\nframeworks"
    assert matches_keywords(text, ["metal-organic framework"])


def test_requires_every_word_of_the_keyword():
    text = "Advances in organic chemistry"
    assert not matches_keywords(text, ["metal-organic framework"])


# --- filter_papers ---------------------------------------------------------


def test_filter_papers_checks_title_and_summary():
    papers = [
        make_paper(
            "1", "Conductive frame-works", summary="New metal-organic frameworks"
        ),
        make_paper("2", "Quantum computing basics"),
    ]
    result = filter_papers(papers, ["metal-organic framework"])
    assert [paper.arxiv_id for paper in result] == ["1"]


def test_filter_papers_sorts_newest_first():
    papers = [
        make_paper("old", "MOF study", published="2026-10-01T00:00:00Z"),
        make_paper("new", "MOF study", published="2026-10-06T00:00:00Z"),
    ]
    result = filter_papers(papers, ["mof"])
    assert [paper.arxiv_id for paper in result] == ["new", "old"]


def test_filter_papers_removes_duplicates():
    papers = [make_paper("1", "MOF study"), make_paper("1", "MOF study")]
    assert len(filter_papers(papers, ["mof"])) == 1
