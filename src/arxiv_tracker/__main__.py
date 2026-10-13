"""Command-line entry point: python -m arxiv_tracker"""

from datetime import UTC, datetime
from pathlib import Path

from arxiv_tracker.config import load_config
from arxiv_tracker.fetch import fetch_papers
from arxiv_tracker.filters import filter_papers
from arxiv_tracker.render import render_page


def main() -> None:
    config = load_config(Path("config.toml"))
    papers = fetch_papers(config.keywords, config.max_results)
    papers = filter_papers(papers, config.keywords)

    output = Path("site") / "index.html"
    output.parent.mkdir(exist_ok=True)
    html = render_page(papers, config.keywords, datetime.now(UTC))
    output.write_text(html, encoding="utf-8")

    print(f"Wrote {len(papers)} papers to {output}")


if __name__ == "__main__":
    main()
