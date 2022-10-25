import concurrent
import re
import threading
import time
import timeit
import urllib.parse

from abc import abstractmethod, ABC
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from requests import Session
from tqdm import tqdm
from typing import List

from page_ranker_app import settings
from page_ranker_app.source import crawlers, inverters, parsers


class PageRankInfoAccumulator(ABC):
    """
    an interface for scrapping of URLs and counting page rank
    """

    def __init__(self, start_url: str, page_limit: int):
        self._start_url = start_url
        self._page_limit = page_limit
        self._page_links = defaultdict(list)
        self._page_rank = {}

    @property
    def page_rank(self):
        """
        a getter method for _page_rank attribute
        :return: _page_rank value
        """
        return self._page_rank

    @abstractmethod
    def scrap_data_till_limit(self) -> None:
        """
        Method gets data starting from self._start_url page saved on
        initialization until it scraps a number of links equal to
        self._page_limit value and saves collected data in
        self._page_links dictionary

        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def count_page_rank(self) -> None:
        """
        The method counts page rank for pages and saves results
        in self._page_rank dictionary

        :return: None
        """
        raise NotImplementedError


class WikiPageRankInfoAccumulator(PageRankInfoAccumulator):
    """
    a class that organizes processes of scrapping of URLs and counting
    page rank
    """

    url_crawler = crawlers.WikiCrawler
    url_parser = parsers.WikiParser
    dict_inverter = inverters.DictionaryInverterThreading

    def __init__(self, start_url: str, page_limit: int):
        super().__init__(start_url, page_limit)
        self._url_mask = self.get_wiki_url_mask(self._start_url)

    @staticmethod
    def get_wiki_url_mask(url: str):
        """
        method processes a URL and returns a URL mask, that contains
        Scheme, Sub-domain, Domain and Top-level domain

        :param url: a given URK
        :return: a URL mask
        """
        mask = re.search("^(https?://)(?:www\.)?([^:/?\n]+)", url)[0]
        return mask

    def _process_wiki_links(self, links: List[str]):
        """
        method processes internal Wikipedia links by adding a URL mask
        to them which is saved in self._url_mask and replacing inner
        spaces with underscores

        :param links: a list of internal links
        :return: a processed list of internal links
        """
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
        session: Session,
    ) -> List[str]:
        """
        Method scraps data from given URL using Session instance for
        performing request, and returns a list of found internal links

        :param url: given URL
        :param session: a session instance
        :return: a list of found internal links
        """
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
        session: Session,
    ) -> None:
        """
        Method scraps a given URL link, processes collected data and
        writes collected data in self._page_links dictionary while also
        copying found links to a given pool to continue parsing and
        recording current URL as visited to prevent repeated scraping
        Uses a lock to prevent race conditions, and a session instance
        for processing the request

        :param url: given URL
        :param lock:  a lock instance
        :param visited: set of visited URLs
        :param url_pool: a list of URLs to visit
        :param session: a session instance
        :return: None
        """
        if url not in visited:
            with lock:
                visited.add(url)

        if len(self._page_links) < self._page_limit:
            local = threading.local()
            local.start = timeit.default_timer()

            local.links = self.collect_page_data(url, session)
            if local.links:
                local.processed_links = self._process_wiki_links(local.links)
                with lock:
                    self._page_links[url] = local.processed_links
                    url_pool.extend(local.processed_links)

                local.spent_time = timeit.default_timer() - local.start
                if local.spent_time < 1:
                    time.sleep(1 - local.spent_time)

    def scrap_data_till_limit(
        self,
        max_workers: int = settings.THREADS_SCRAPPING,
    ):
        """
        Method gets data starting from self._start_url page saved on
        initialization until it scraps a number of links equal to
        self._page_limit value and then saves collected data in
        self._page_links dictionary
        Uses threading to improve performance

        :param max_workers: max number of active threads
        :return: None
        """
        max_workers = (
            max_workers
            if max_workers <= settings.MAX_REQUESTS_PER_SECOND
            else settings.MAX_REQUESTS_PER_SECOND
        )
        visited = set()
        url_pool = [self._start_url]

        with tqdm(total=self._page_limit) as prog_bar, Session() as session:
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
                        if prog_bar.n < self._page_limit:
                            prog_bar.update(1)

    def count_page_rank(self) -> None:
        """
        The method counts page rank for pages by reversing _page_links
        dictionary key-value pairs, then counting number of links that
        lead to the page and saves results in self._page_rank dictionary

        :return: None
        """
        rev_data = self.dict_inverter().invert_dict(self._page_links)
        self._page_rank = {key: len(value) for key, value in rev_data.items()}


if __name__ == "__main__":
    pass
