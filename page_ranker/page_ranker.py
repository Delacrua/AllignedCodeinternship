import re
import urllib.parse

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from typing import List

import requests

import settings

from utils import crawler, parser


class PageRankInfoAccumulator:

    def __init__(self, start_url: str, page_limit: int):
        self._start_url = start_url
        self._page_limit = page_limit
        self._page_links = defaultdict(list)
        self._page_rank = {}


class WikiPageRankInfoAccumulator(PageRankInfoAccumulator):
    def __init__(self, start_url: str, page_limit: int):
        super().__init__(start_url, page_limit)
        self.url_crawler = crawler.WikiCrawler
        self.url_parser = parser.WikiParser
        self._url_mask = self.get_wiki_url_mask(self._start_url)

    @staticmethod
    def get_wiki_url_mask(url: str):
        mask = re.search(
            '^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)',
            url
        )[0]
        return mask

    def _process_wiki_links(self, links: List[str]):
        processed_links = [urllib.parse.urljoin(self._url_mask, link)
                           for link in links]
        processed_links = [link.strip().replace(' ', '_') for link in processed_links]
        return processed_links

    def collect_page_data(self, url: str, session: requests.Session) -> List[str]:
        url_crawler = self.url_crawler()
        url_parser = self.url_parser()
        request_text = url_crawler(url, session)
        internal_links = url_parser.parse(request_text)
        return internal_links

    def run_single_time(self, url: str, visited: set, url_pool: list, session: requests.Session):
        if url not in visited:
            visited.add(url)
        if len(self._page_links) < self._page_limit:
            links = self.collect_page_data(url, session)
            processed_links = self._process_wiki_links(links)
            self._page_links[url] = processed_links
            url_pool.extend(processed_links)

    def collect_data_till_limit(self):
        session = requests.Session()
        visited = set()
        url_pool = [self._start_url]
        while len(self._page_links) < self._page_limit:
            link_pool_for_workers = url_pool[:]
            url_pool.clear()
            with ThreadPoolExecutor(max_workers=50) as executor:
                executor.map(self.run_single_time,
                             link_pool_for_workers,
                             repeat(visited),
                             repeat(url_pool),
                             repeat(session)
                             )

    def count_page_rank(self):
        """
        The function counts page rank for wiki pages by reversing
        dictionaries key-value pairs in a way that
        each string from the lists of values becomes a key, and keys of the
        original key-value pairs are put into lists of values for new keys
        and saves results as
        :return:
        """
        rev_data = {}
        for key, values in self._page_links.items():
            for value in values:
                rev_data[value] = rev_data.get(value, [])
                rev_data[value].append(key)
        self._page_rank = {key: len(value) for key, value in rev_data.items()}


if __name__ == '__main__':
    wiki_scrapper = WikiPageRankInfoAccumulator(
        'https://en.wikipedia.org/wiki/Superintendent', 100)
    wiki_scrapper.collect_data_till_limit()
    wiki_scrapper.count_page_rank()
    print(wiki_scrapper._page_rank)
