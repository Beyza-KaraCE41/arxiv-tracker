"""Filter and sort papers by keywords."""

from arxiv_tracker.fetch import Paper
from arxiv_tracker.text import tokenize

MAX_SPAN = 5


def matches_keywords(text: str, keywords: list[str]) -> bool:
    """Return True if the text matches any of the keywords.

    A keyword matches when all of its words appear close together in the
    text: the first and last matching word may be at most MAX_SPAN words
    apart. A word matches exactly or as the start of a longer word
    ("framework" matches "frameworks"). Case, hyphens and punctuation are
    ignored.
    """
    words = tokenize(text)
    for keyword in keywords:
        terms = tokenize(keyword)
        if terms and _terms_close_together(words, terms):
            return True
    return False


def _terms_close_together(words: list[str], terms: list[str]) -> bool:
    """Return True if every term occurs within a window of MAX_SPAN words."""
    positions = [
        [index for index, word in enumerate(words) if word.startswith(term)]
        for term in terms
    ]
    if not all(positions):
        return False
    starts = sorted({index for term_positions in positions for index in term_positions})
    for start in starts:
        if all(
            any(start <= index <= start + MAX_SPAN for index in term_positions)
            for term_positions in positions
        ):
            return True
    return False


def filter_papers(papers: list[Paper], keywords: list[str]) -> list[Paper]:
    """Keep papers whose title or summary matches a keyword.

    Duplicates are removed and the result is sorted newest first.
    """
    seen: set[str] = set()
    result = []
    for paper in papers:
        if paper.arxiv_id in seen:
            continue
        if matches_keywords(f"{paper.title} {paper.summary}", keywords):
            seen.add(paper.arxiv_id)
            result.append(paper)
    return sorted(result, key=lambda paper: paper.published, reverse=True)
