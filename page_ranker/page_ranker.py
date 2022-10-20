import re
import time
import urllib.parse

from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor
from typing import List

import settings

from utils import crawler, parser


class PageRankInfoAccumulator:

    def __init__(self, start_url: str, page_limit: int):
        self._start_url = start_url
        self._page_limit = page_limit
        self._page_links = defaultdict(list)
        self._page_rank = defaultdict(list)


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
        return processed_links

    def collect_page_data(self, url: str) -> List[str]:
        url_crawler = self.url_crawler()
        url_parser = self.url_parser()
        request_text = url_crawler(url)
        internal_links = url_parser.parse(request_text)
        return internal_links

    def run_single_time(self, url: str, visited: set, url_pool: list):
        if url not in visited:
            visited.add(url)
            links = self.collect_page_data(url)
            processed_links = self._process_wiki_links(links)
            self._page_links[url] = processed_links
            url_pool.extend(processed_links)

    def collect_data_till_limit(self):
        visited = set()
        url_pool = [self._start_url]
        while len(visited) < self._page_limit:
            link_pool_for_workers = url_pool[:]
            url_pool.clear()
            with ThreadPoolExecutor(max_workers=10) as executor:
                executor.map(self.run_single_time,
                             link_pool_for_workers,
                             visited,
                             url_pool)


def main():
    wiki_scrapper = WikiPageRankInfoAccumulator('https://en.wikipedia.org/wiki/California_Distinguished_School', 10)
    visited = set()
    url_pool = []
    wiki_scrapper.run_single_time('https://en.wikipedia.org/wiki/California_Distinguished_School', visited, url_pool)
    print(wiki_scrapper._page_links)


if __name__ == '__main__':
    main()
