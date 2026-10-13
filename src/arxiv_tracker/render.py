"""Render papers as a static HTML page."""

from datetime import datetime
from html import escape

from arxiv_tracker.fetch import Paper

STYLE = """
body { font-family: system-ui, sans-serif; max-width: 760px; margin: 2rem auto;
       padding: 0 1rem; line-height: 1.5; color: #222; }
.meta { color: #666; font-size: 0.9rem; }
article { border-top: 1px solid #ddd; padding: 1rem 0; }
article h2 { font-size: 1.1rem; margin: 0 0 0.3rem; }
article p { margin: 0.3rem 0; }
.authors { color: #555; font-size: 0.9rem; }
"""


def render_paper(paper: Paper) -> str:
    """Render a single paper as an HTML <article> block."""
    authors = ", ".join(paper.authors)
    date = paper.published[:10]
    return (
        "<article>\n"
        f'  <h2><a href="{escape(paper.url)}">{escape(paper.title)}</a></h2>\n'
        f'  <p class="meta">{escape(date)} · {escape(paper.arxiv_id)}</p>\n'
        f'  <p class="authors">{escape(authors)}</p>\n'
        f"  <p>{escape(paper.summary)}</p>\n"
        "</article>"
    )


def render_page(papers: list[Paper], keywords: list[str], updated: datetime) -> str:
    """Render the full HTML page."""
    if papers:
        items = "\n".join(render_paper(paper) for paper in papers)
    else:
        items = "<p>No matching papers found.</p>"
    keyword_text = escape(", ".join(keywords))
    updated_text = updated.strftime("%Y-%m-%d %H:%M")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>arXiv Tracker</title>
<style>{STYLE}</style>
</head>
<body>
<h1>arXiv Tracker</h1>
<p class="meta">Keywords: {keyword_text} · Updated {updated_text} UTC · {len(papers)} papers</p>
{items}
</body>
</html>
"""
