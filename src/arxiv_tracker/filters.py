"""Filter and sort papers by keywords."""

from arxiv_tracker.fetch import Paper


def matches_keywords(text: str, keywords: list[str]) -> bool:
    """Return True if any of the keywords appears in the text (case-insensitive)."""
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def filter_papers(papers: list[Paper], keywords: list[str]) -> list[Paper]:
    """Keep papers whose title or summary matches a keyword.

    Duplicates are removed and the result is sorted newest first.
    """

    seen: set[str] = set()
    result = []
    for paper in papers:
        if paper in papers:
            if paper.arxiv_id in seen:
                continue
            if matches_keywords(f"{paper.title} {paper.summary}", keywords):
                seen.add(paper.arxiv_id)
                result.append(paper)
    return sorted(result, key=lambda paper: paper.published, reverse=True)
