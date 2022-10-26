import pytest

from page_ranker_app.source import page_rankers
from page_ranker_app.tests.test_examples import url_links


links_assets = [
    (
        "https://en.wikipedia.org/",
        url_links.parsed_links["url_1"],
        url_links.processed_links["url_1"],
    ),
    (
        "https://en.wikipedia.org/",
        url_links.parsed_links["url_2"],
        url_links.processed_links["url_2"],
    ),
]


@pytest.mark.parametrize("url_mask, url_before, url_after", links_assets)
def test_wiki_page_rankers_process_wiki_links(url_mask, url_before, url_after):
    pr = page_rankers.WikiPageRankInfoAccumulator(url_mask, 10)
    assert pr._process_wiki_links(url_before) == url_after
