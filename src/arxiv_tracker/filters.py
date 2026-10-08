def matches_keywords(text: str, keywords: list[str]) -> bool:
    """Return True if any of the keywords appears in the text (case-insensitive)."""
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)
