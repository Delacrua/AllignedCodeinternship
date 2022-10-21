import re
import threading
import time
import timeit

import requests
import urllib.parse

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from typing import List

import settings

from source import crawler, parser


class PageRankInfoAccumulator:

    def __init__(self, start_url: str, page_limit: int):
        self._start_url = start_url
        self._page_limit = page_limit
        self._page_links = defaultdict(list)
        self._page_rank = {}

    @property
    def page_rank(self):
        return self._page_rank


class WikiPageRankInfoAccumulator(PageRankInfoAccumulator):
    def __init__(self, start_url: str, page_limit: int):
        super().__init__(start_url, page_limit)
        self.url_crawler = crawler.WikiCrawler
        self.url_parser = parser.WikiParser
        self._url_mask = self.get_wiki_url_mask(self._start_url)

    @staticmethod
    def get_wiki_url_mask(url: str):
        mask = re.search('^(https?://)(?:www\.)?([^:/?\n]+)', url)[0]
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

    def scrap_one_url(self, url: str, visited: set, url_pool: list, session: requests.Session):
        if url not in visited:
            visited.add(url)

        if len(self._page_links) < self._page_limit:
            local = threading.local()
            local.start = timeit.default_timer()

            links = self.collect_page_data(url, session)
            processed_links = self._process_wiki_links(links)
            self._page_links[url] = processed_links
            url_pool.extend(processed_links)

            local.spent_time = timeit.default_timer() - local.start
            if local.spent_time < 1:
                time.sleep(1 - local.spent_time)

    def scrap_data_till_limit(self, max_workers: int = settings.WORKERS_SCRAPPING):
        max_workers = max_workers if max_workers <= settings.MAX_REQUESTS_PER_SECOND else settings.MAX_REQUESTS_PER_SECOND
        session = requests.Session()
        visited = set()
        url_pool = [self._start_url]
        while len(self._page_links) < self._page_limit:
            link_pool_for_workers = url_pool[:]
            url_pool.clear()
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                executor.map(self.scrap_one_url,
                             link_pool_for_workers,
                             repeat(visited),
                             repeat(url_pool),
                             repeat(session)
                             )
        session.close()

    def count_page_rank(self):
        """
        The method counts page rank for wiki pages by reversing
        dictionaries key-value pairs in a way that each string from
        the lists of values becomes a key, and keys of the original
        key-value pairs are put into lists of values for new keys
        and saves results in objects _page_rank dictionary
        :return:
        """
        rev_data = {}
        for key, values in self._page_links.items():
            for value in values:
                rev_data[value] = rev_data.get(value, [])
                rev_data[value].append(key)
        self._page_rank = {key: len(value) for key, value in rev_data.items()}


def main(url: str, limit: int):
    wiki_scrapper = WikiPageRankInfoAccumulator(url, limit)
    wiki_scrapper.scrap_data_till_limit()
    wiki_scrapper.count_page_rank()
    print(wiki_scrapper.page_rank)


if __name__ == '__main__':
    test_url = 'https://en.wikipedia.org/wiki/Superintendent'
    test_limit = 100
    main(test_url, test_limit)
