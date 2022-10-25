from abc import ABC, abstractmethod
from typing import List

from bs4 import BeautifulSoup


class Parser(ABC):
    """
    an interface for Parser class
    """
    @abstractmethod
    def parse(self, request_text: str) -> List[str]:
        raise NotImplementedError


class WikiParser(Parser):
    """
    a class that processes data from Wikipedia pages
    """
    def parse(self, request_text: str) -> List[str]:
        """
        method for parsing and processing of Wikipedia page data, it
        collects and returns a list of links on internal resources

        :param request_text: Wikipedia page data in string form
        :return: a list of links on internal resources
        """
        _soup = BeautifulSoup(request_text, "html.parser")
        internal_url_links = []

        for link in _soup.find_all("a", href=True):
            if link.get("href").startswith("/wiki/") and ":" not in link.get(
                "href"
            ):
                internal_url_links.append(link["href"])
        return internal_url_links


if __name__ == "__main__":
    pass
