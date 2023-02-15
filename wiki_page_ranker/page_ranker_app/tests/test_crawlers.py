import pytest

from functools import wraps
from requests import HTTPError
from unittest import mock

from page_ranker_app import settings
from page_ranker_app.source.utils import mock_decorator as mock_deco

mock.patch("page_ranker_app.source.utils.handle_errors", mock_deco).start()

from page_ranker_app.source.crawlers import WikiCrawler

code_assets = [
    (
        200,
        "I am mocked text",
        "I am mocked text",
    ),
    (
        404,
        "I am mocked text",
        settings.NOT_SET,
    ),
]


@pytest.mark.parametrize("response_code, response_text, expected", code_assets)
def test_wiki_crawler_call_text(response_code, response_text, expected):
    mock_session = mock.MagicMock()
    mock_response = mock.MagicMock()
    mock_session.get.return_value = mock_response

    mock_response.status_code = response_code
    mock_response.text = response_text
    url = "someurl"

    crawler = WikiCrawler()
    with mock_session:
        assert crawler(url, mock_session) == expected


code_assets_exception = [
    500,
    305,
    101,
]


@pytest.mark.parametrize("response_code", code_assets_exception)
def test_wiki_crawler_call_exceptions(response_code):
    mock_session = mock.MagicMock()
    mock_response = mock.MagicMock()
    mock_session.get.return_value = mock_response

    mock_response.status_code = response_code
    url = "someurl"

    crawler = WikiCrawler()
    with mock_session, pytest.raises(HTTPError):
        crawler(url, mock_session)
