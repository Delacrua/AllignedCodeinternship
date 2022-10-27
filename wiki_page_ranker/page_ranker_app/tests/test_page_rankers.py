import pathlib
import threading

import pytest

from unittest import mock

from page_ranker_app.source import page_rankers
from page_ranker_app.tests.test_examples import url_links

cur_path = pathlib.Path(__file__).resolve().parent

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
def test_wiki_page_ranker_process_wiki_links(url_mask, url_before, url_after):
    pr = page_rankers.WikiPageRankInfoAccumulator(url_mask, 10)
    assert pr._process_wiki_links(url_before) == url_after


page_data_assets = [
    (
        "https://en.wikipedia.org/",
        cur_path / "test_examples/url_text1.html",
        url_links.parsed_links["url_1"],
    ),
    (
        "https://en.wikipedia.org/",
        cur_path / "test_examples/url_text2.html",
        url_links.parsed_links["url_2"],
    ),
]


@pytest.mark.parametrize("url, url_text_source, expected", page_data_assets)
def test_wiki_page_ranker_collect_page_data(url, url_text_source, expected):
    mock_session = mock.MagicMock()
    mock_response = mock.MagicMock()
    mock_session.get.return_value = mock_response

    mock_response.status_code = 200
    with open(url_text_source) as source:
        mock_response.text = source.read()

    page_ranker = page_rankers.WikiPageRankInfoAccumulator(url, 1)
    assert page_ranker.collect_page_data(url, mock_session) == expected


scrap_assets = [
    (
        "https://en.wikipedia.org/url_1",
        cur_path / "test_examples/url_text1.html",
        (
            {"https://en.wikipedia.org/url_1"},
            url_links.processed_links["url_1"],
        ),
    ),
    (
        "https://en.wikipedia.org/url_2",
        cur_path / "test_examples/url_text2.html",
        (
            {"https://en.wikipedia.org/url_2"},
            url_links.processed_links["url_2"],
        ),
    ),
]


@pytest.mark.parametrize("url, url_text_source, expected", scrap_assets)
def test_wiki_page_ranker_scrap_one_url(url, url_text_source, expected):
    mock_session = mock.MagicMock()
    mock_response = mock.MagicMock()
    mock_session.get.return_value = mock_response

    mock_response.status_code = 200
    with open(url_text_source) as source:
        mock_response.text = source.read()

    page_ranker = page_rankers.WikiPageRankInfoAccumulator(url, 1)
    lock = threading.Lock()
    visited = set()
    url_pool = []
    page_ranker.scrap_one_url(url, lock, visited, url_pool, mock_session)
    assert (visited, url_pool) == expected


page_rank_assets = [
    (
        {"a": ["url1"], "b": ["url3", "url5"], "c": ["url4"]},
        {"url1": 1, "url3": 1, "url5": 1, "url4": 1},
    ),
    (
        {"a": ["url1", "url2"], "b": ["url3", "url4"], "c": ["url4"]},
        {"url1": 1, "url2": 1, "url3": 1, "url4": 2},
    ),
]


@pytest.mark.parametrize("source_dict, expected", page_rank_assets)
def test_wiki_page_ranker_count_page_rank(source_dict, expected):
    url = 'https://en.wikipedia.org/'
    page_ranker = page_rankers.WikiPageRankInfoAccumulator(url, 1)
    page_ranker._page_links = source_dict
    page_ranker.count_page_rank()
    assert page_ranker.page_rank == expected
