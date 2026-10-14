"""Command-line entry point: python -m arxiv_tracker"""

from datetime import UTC, datetime
from pathlib import Path

from arxiv_tracker.config import load_config
from arxiv_tracker.fetch import fetch_papers
from arxiv_tracker.filters import filter_papers
from arxiv_tracker.history import find_new_ids, load_previous_ids, save_ids
from arxiv_tracker.render import render_page


def main() -> None:
    config = load_config(Path("config.toml"))
    papers = fetch_papers(config.keywords, config.max_results)
    papers = filter_papers(papers, config.keywords)

    previous_ids = None
    if config.site_url:
        previous_ids = load_previous_ids(config.site_url.rstrip("/") + "/papers.json")
    new_ids = find_new_ids(papers, previous_ids)

    site = Path("site")
    site.mkdir(exist_ok=True)
    html = render_page(papers, config.keywords, datetime.now(UTC), new_ids)
    (site / "index.html").write_text(html, encoding="utf-8")
    save_ids(papers, site / "papers.json")

    print(f"Wrote {len(papers)} papers ({len(new_ids)} new) to {site}")


if __name__ == "__main__":
    main()
