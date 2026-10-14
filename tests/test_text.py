from arxiv_tracker.text import tokenize


def test_tokenize_splits_on_hyphens_and_punctuation():
    words = tokenize("Metal-Organic Frameworks (MOFs), 2D!")
    assert words == ["metal", "organic", "frameworks", "mofs", "2d"]


def test_tokenize_handles_line_breaks_and_extra_spaces():
    assert tokenize("  conductive\n  frame-works ") == ["conductive", "frame", "works"]


def test_tokenize_empty_text():
    assert tokenize("") == []
