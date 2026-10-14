"""Filter and sort papers by keywords."""

from arxiv_tracker.fetch import Paper
from arxiv_tracker.text import tokenize


def matches_keywords(text: str, keywords: list[str]) -> bool:
    """Return True if the text matches any of the keywords.

    A keyword matches when every word in it appears in the text, either
    exactly or as the start of a longer word ("framework" matches
    "frameworks"). Case, hyphens and punctuation are ignored.
    """
    words = tokenize(text)
    for keyword in keywords:
        terms = tokenize(keyword)
        if terms and all(_has_word(words, term) for term in terms):
            return True
    return False


def _has_word(words: list[str], term: str) -> bool:
    """Return True if any word equals the term or starts with it."""
    return any(word.startswith(term) for word in words)


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
