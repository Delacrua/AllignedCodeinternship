import pathlib

import pytest

from page_ranker_app.source import parsers
from page_ranker_app.tests.test_examples import url_links


cur_path = pathlib.Path(__file__).resolve().parent

parsing_assets = [
    (
        cur_path / "test_examples/url_text1.html",
        url_links.parsed_links["url_1"],
    ),
    (
        cur_path / "test_examples/url_text2.html",
        url_links.parsed_links["url_2"],
    ),
]


@pytest.mark.parametrize("source_text, expected", parsing_assets)
def test_wiki_parser_parse(source_text, expected):
    parser = parsers.WikiParser()
    with open(source_text) as source:
        assert parser.parse(source.read()) == expected
