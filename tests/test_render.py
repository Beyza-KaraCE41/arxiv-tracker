from datetime import UTC, datetime

from arxiv_tracker.fetch import Paper
from arxiv_tracker.render import format_authors, render_page, render_paper

UPDATED = datetime(2026, 10, 13, 9, 0, tzinfo=UTC)


def make_paper(title: str = "MOF study") -> Paper:
    return Paper(
        arxiv_id="2610.00001v1",
        title=title,
        summary="A short summary.",
        authors=["Ada Lovelace", "José Real"],
        published="2026-10-06T15:26:30Z",
        url="https://arxiv.org/abs/2610.00001v1",
    )


# --- render_paper ----------------------------------------------------------


def test_render_paper_contains_title_link_and_authors():
    html = render_paper(make_paper())

    assert '<a href="https://arxiv.org/abs/2610.00001v1">MOF study</a>' in html
    assert "Ada Lovelace, José Real" in html
    assert "2026-10-06" in html


def test_render_paper_links_to_pdf():
    html = render_paper(make_paper())
    assert 'href="https://arxiv.org/pdf/2610.00001v1"' in html


def test_render_paper_escapes_html_in_title():
    html = render_paper(make_paper(title="Pore size < 2 nm & <b>bold</b>"))

    assert "Pore size &lt; 2 nm &amp; &lt;b&gt;bold&lt;/b&gt;" in html
    assert "<b>" not in html


# --- format_authors --------------------------------------------------------


def test_format_authors_keeps_short_lists():
    assert format_authors(["A", "B"]) == "A, B"


def test_format_authors_shortens_long_lists():
    authors = [f"Author {number}" for number in range(10)]
    result = format_authors(authors)

    assert result.startswith("Author 0, Author 1")
    assert result.endswith("Author 5 et al.")
    assert "Author 6" not in result


# --- render_page -----------------------------------------------------------


def test_render_page_shows_count_keywords_and_date():
    page = render_page([make_paper(), make_paper()], ["mof", "linker"], UPDATED)

    assert "of 2 papers" in page
    assert '<span class="chip">mof</span>' in page
    assert '<span class="chip">linker</span>' in page
    assert "2026-10-13 09:00 UTC" in page


def test_render_page_with_no_papers_shows_message():
    page = render_page([], ["mof"], UPDATED)
    assert "No matching papers found." in page
