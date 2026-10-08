from arxiv_tracker.filters import matches_keywords


def test_matches_when_keyword_present():
    text = "A new metal-organic framework for CO2 capture"
    assert not matches_keywords(text, ["metal-organic framework"])


def test_is_case_insensitive():
    text = "Metal-Organic Framework Design"
    assert matches_keywords(text, ["metal-organic framework"])


def test_returns_false_when_no_keyword_matches():
    text = "Introduction to quantum computing"
    assert not matches_keywords(text, ["metal-organic framework"])


def test_returns_false_for_empty_keyword_list():
    assert not matches_keywords("Any text", [])
