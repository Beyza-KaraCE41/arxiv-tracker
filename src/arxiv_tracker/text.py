"""Helpers for splitting text into normalized words."""

import re

_NON_WORD = re.compile(r"[^a-z0-9]+")


def tokenize(text: str) -> list[str]:
    """Lowercase the text and split it into words.

    Hyphens, punctuation and line breaks all count as separators,
    so "Metal-Organic" becomes ["metal", "organic"].
    """
    return [word for word in _NON_WORD.split(text.lower()) if word]
