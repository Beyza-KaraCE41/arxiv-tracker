from pathlib import Path

from arxiv_tracker.config import load_config

REPO_CONFIG = Path(__file__).parent.parent / "config.toml"


def test_load_config_reads_keywords_and_max_results(tmp_path):
    config_file = tmp_path / "config.toml"
    config_file.write_text(
        '[search]\nkeywords = ["mof", "linker"]\nmax_results = 10\n',
        encoding="utf-8",
    )

    config = load_config(config_file)

    assert config.keywords == ["mof", "linker"]
    assert config.max_results == 10


def test_load_config_uses_defaults_for_optional_settings(tmp_path):
    config_file = tmp_path / "config.toml"
    config_file.write_text('[search]\nkeywords = ["mof"]\n', encoding="utf-8")

    config = load_config(config_file)

    assert config.max_results == 50
    assert config.site_url == ""


def test_load_config_reads_site_url(tmp_path):
    config_file = tmp_path / "config.toml"
    config_file.write_text(
        '[search]\nkeywords = ["mof"]\n\n[site]\nurl = "https://example.com/"\n',
        encoding="utf-8",
    )

    assert load_config(config_file).site_url == "https://example.com/"


def test_repository_config_is_valid():
    config = load_config(REPO_CONFIG)
    assert config.keywords
