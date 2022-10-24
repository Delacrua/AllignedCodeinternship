from abc import ABC, abstractmethod
from typing import List

from bs4 import BeautifulSoup


class Parser(ABC):
    @abstractmethod
    def parse(self, request_text: str) -> List[str]:
        raise NotImplementedError


class WikiParser(Parser):
    def parse(self, request_text: str) -> List[str]:
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
