"""Render papers as a static HTML page."""

from datetime import datetime
from html import escape

from arxiv_tracker.fetch import Paper

MAX_AUTHORS = 6
REPO_URL = "https://github.com/Beyza-KaraCE41/arxiv-tracker"

STYLE = """
:root {
  --bg: #f6f7fb; --card: #ffffff; --text: #1f2330; --muted: #6b7185;
  --accent: #3b5bdb; --accent-soft: #e7ecff; --border: #e3e6ef; --new: #2f9e44;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #12141b; --card: #1b1e27; --text: #e6e8ef; --muted: #9aa0b4;
    --accent: #8ea2ff; --accent-soft: #262c45; --border: #2a2e3b; --new: #51cf66;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--bg); color: var(--text); line-height: 1.55;
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
}
.wrap { max-width: 820px; margin: 0 auto; padding: 0 1rem; }
header {
  position: sticky; top: 0; z-index: 1; background: var(--bg);
  border-bottom: 1px solid var(--border); padding: 1rem 0;
}
h1 { margin: 0; font-size: 1.5rem; }
.meta { color: var(--muted); font-size: 0.875rem; margin: 0.2rem 0; }
.meta strong { color: var(--new); }
.chips { display: flex; flex-wrap: wrap; gap: 0.4rem; margin: 0.6rem 0; }
.chip {
  background: var(--accent-soft); color: var(--accent); border-radius: 999px;
  padding: 0.15rem 0.7rem; font-size: 0.8rem;
}
#search {
  width: 100%; padding: 0.6rem 0.8rem; border: 1px solid var(--border);
  border-radius: 8px; background: var(--card); color: var(--text); font-size: 0.95rem;
}
main { padding: 1.2rem 1rem 2rem; }
.card {
  background: var(--card); border: 1px solid var(--border); border-radius: 12px;
  padding: 1rem 1.2rem; margin-bottom: 0.9rem;
}
.card.new { border-left: 4px solid var(--new); }
.card h2 { font-size: 1.05rem; margin: 0 0 0.35rem; line-height: 1.4; }
.card h2 a { color: var(--text); text-decoration: none; }
.card h2 a:hover { color: var(--accent); }
.authors { color: var(--muted); font-size: 0.875rem; margin: 0.2rem 0 0.5rem; }
.actions { display: flex; gap: 0.6rem; align-items: center; flex-wrap: wrap; }
.btn {
  font-size: 0.8rem; padding: 0.2rem 0.65rem; border: 1px solid var(--border);
  border-radius: 6px; color: var(--accent); text-decoration: none;
}
.btn:hover { background: var(--accent-soft); }
.badge {
  background: var(--new); color: #fff; border-radius: 6px;
  padding: 0.1rem 0.5rem; font-size: 0.75rem; font-weight: 600;
}
details { margin-top: 0.5rem; }
summary { cursor: pointer; color: var(--muted); font-size: 0.875rem; }
details p { margin: 0.5rem 0 0; }
.empty { text-align: center; color: var(--muted); padding: 2rem 0; }
footer { color: var(--muted); font-size: 0.8rem; text-align: center; padding: 0 1rem 2rem; }
footer a { color: var(--accent); }
"""

SCRIPT = """
const input = document.getElementById("search");
const cards = document.querySelectorAll(".card");
const counter = document.getElementById("visible-count");
input.addEventListener("input", () => {
  const query = input.value.trim().toLowerCase();
  let visible = 0;
  cards.forEach((card) => {
    const match = card.textContent.toLowerCase().includes(query);
    card.hidden = !match;
    if (match) visible++;
  });
  counter.textContent = visible;
});
"""


def format_authors(authors: list[str]) -> str:
    """Join author names, shortening long lists with 'et al.'."""
    if len(authors) > MAX_AUTHORS:
        return ", ".join(authors[:MAX_AUTHORS]) + " et al."
    return ", ".join(authors)


def pdf_url(abs_url: str) -> str:
    """Turn an arXiv abstract URL into the matching PDF URL."""
    return abs_url.replace("/abs/", "/pdf/")


def render_paper(paper: Paper, is_new: bool = False) -> str:
    """Render a single paper as an HTML card."""
    date = paper.published[:10]
    card_class = "card new" if is_new else "card"
    badge = '<span class="badge">New</span>' if is_new else ""
    return f"""<article class="{card_class}">
  <h2><a href="{escape(paper.url)}">{escape(paper.title)}</a></h2>
  <p class="authors">{escape(format_authors(paper.authors))}</p>
  <div class="actions">
    {badge}
    <span class="meta">{escape(date)} · {escape(paper.arxiv_id)}</span>
    <a class="btn" href="{escape(pdf_url(paper.url))}">PDF</a>
  </div>
  <details>
    <summary>Abstract</summary>
    <p>{escape(paper.summary)}</p>
  </details>
</article>"""


def render_page(
    papers: list[Paper],
    keywords: list[str],
    updated: datetime,
    new_ids: set[str] | None = None,
) -> str:
    """Render the full HTML page.

    Papers whose IDs are in new_ids get a "New" badge.
    """
    new_ids = new_ids or set()
    if papers:
        items = "\n".join(
            render_paper(paper, is_new=paper.arxiv_id in new_ids) for paper in papers
        )
    else:
        items = '<p class="empty">No matching papers found.</p>'
    chips = "".join(f'<span class="chip">{escape(word)}</span>' for word in keywords)
    updated_text = updated.strftime("%Y-%m-%d %H:%M")
    count = len(papers)
    new_count = sum(1 for paper in papers if paper.arxiv_id in new_ids)
    new_text = f" · <strong>{new_count} new</strong>" if new_count else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>arXiv Tracker</title>
<style>{STYLE}</style>
</head>
<body>
<header>
  <div class="wrap">
    <h1>arXiv Tracker</h1>
    <p class="meta">Updated {updated_text} UTC ·
      <span id="visible-count">{count}</span> of {count} papers{new_text}</p>
    <div class="chips">{chips}</div>
    <input id="search" type="search" aria-label="Filter papers"
      placeholder="Filter by title, author or abstract...">
  </div>
</header>
<main class="wrap">
{items}
</main>
<footer class="wrap">
  Updated daily with GitHub Actions · <a href="{REPO_URL}">Source on GitHub</a>
</footer>
<script>{SCRIPT}</script>
</body>
</html>
"""
