import concurrent
import re
import requests
import threading
import time
import timeit
import urllib.parse

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from typing import List

from tqdm import tqdm

from page_ranker_app import settings
from page_ranker_app.source import crawlers, inverters, parsers


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
    url_crawler = crawlers.WikiCrawler
    url_parser = parsers.WikiParser
    dict_inverter = inverters.DictionaryInverterThreading

    def __init__(self, start_url: str, page_limit: int):
        super().__init__(start_url, page_limit)
        self._url_mask = self.get_wiki_url_mask(self._start_url)

    @staticmethod
    def get_wiki_url_mask(url: str):
        mask = re.search("^(https?://)(?:www\.)?([^:/?\n]+)", url)[0]
        return mask

    def _process_wiki_links(self, links: List[str]):
        processed_links = [
            urllib.parse.urljoin(self._url_mask, link) for link in links
        ]
        processed_links = [
            link.strip().replace(" ", "_") for link in processed_links
        ]
        return processed_links

    def collect_page_data(
        self,
        url: str,
        session: requests.Session,
    ) -> List[str]:
        url_crawler = self.url_crawler()
        url_parser = self.url_parser()
        request_text = url_crawler(url, session)
        if not isinstance(request_text, settings.NotSet):
            internal_links = url_parser.parse(request_text)
            return internal_links

    def scrap_one_url(
        self,
        url: str,
        lock: threading.Lock,
        visited: set,
        url_pool: list,
        session: requests.Session,
    ):
        if url not in visited:
            with lock:
                visited.add(url)

        if len(self._page_links) < self._page_limit:
            local = threading.local()
            local.start = timeit.default_timer()

            local.links = self.collect_page_data(url, session)
            if local.links:
                local.processed_links = self._process_wiki_links(local.links)
                self._page_links[url] = local.processed_links
                with lock:
                    url_pool.extend(local.processed_links)

                local.spent_time = timeit.default_timer() - local.start
                if local.spent_time < 1:
                    time.sleep(1 - local.spent_time)

    def scrap_data_till_limit(
        self,
        max_workers: int = settings.THREADS_SCRAPPING,
    ):
        max_workers = (
            max_workers
            if max_workers <= settings.MAX_REQUESTS_PER_SECOND
            else settings.MAX_REQUESTS_PER_SECOND
        )
        visited = set()
        url_pool = [self._start_url]
        with tqdm(
            total=self._page_limit
        ) as pbar, requests.Session() as session:
            lock = threading.Lock()

            while len(self._page_links) < self._page_limit:
                diff = self._page_limit - len(self._page_links)
                if len(url_pool) < diff:
                    link_pool_for_workers = url_pool[:]
                    url_pool.clear()
                else:
                    link_pool_for_workers = url_pool[:diff]
                    url_pool[:diff] = []

                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    futures = []
                    for url in link_pool_for_workers:
                        futures.append(
                            executor.submit(
                                self.scrap_one_url,
                                url,
                                lock,
                                visited,
                                url_pool,
                                session,
                            )
                        )
                    for _ in concurrent.futures.as_completed(futures):
                        if pbar.n < self._page_limit:
                            pbar.update(1)

    def count_page_rank(self):
        """
        The method counts page rank for wiki pages by reversing
        _page_links dictionaries key-value pairs in a way that each
        string from the lists of values becomes a key, and keys of the
        original key-value pairs are put into lists of values for new
        keys and saves results in objects _page_rank dictionary
        :return:
        """
        rev_data = self.dict_inverter().invert_dict(self._page_links)
        self._page_rank = {key: len(value) for key, value in rev_data.items()}


if __name__ == "__main__":
    pass
