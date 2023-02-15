import requests

from abc import ABC, abstractmethod
from typing import Union

from requests import HTTPError

from page_ranker_app import settings
from page_ranker_app.source.utils import handle_errors
from page_ranker_app.source.loggers import crawler_logger


class Crawler(ABC):
    """
    an interface for Crawler class
    """

    def __init__(
        self,
        timeout: Union[int, float] = settings.REQUEST_TIMEOUT,
        default: Union[str, None, settings.NotSet] = settings.NOT_SET,
    ):
        """
        object constructor, utilizing a property for value validation
        and conversion

        :param timeout: a timeout for making a request in seconds
        :param default: a default value for whenever a request fails
        with 404 status
        """
        self.timeout = timeout
        self.default = default

    @property
    def timeout(self) -> Union[int, float]:
        """
        getter for timeout attribute

        :return: timeout attribute value
        """
        return self._timeout

    @timeout.setter
    def timeout(self, new_value: Union[int, float]) -> None:
        """
        setter for timeout attribute

        :param new_value: new value for timeout attribute
        :return: None
        """
        if not isinstance(new_value, (int, float)):
            raise ValueError("Given timeout value is not int or float")
        else:
            self._timeout = new_value

    @abstractmethod
    def __call__(
        self,
        url: str,
        session: requests.Session,
    ) -> Union[str, None, settings.NotSet]:
        raise NotImplementedError


class WikiCrawler(Crawler):
    """
    a callable class that allows making requests to a URL
    """

    @handle_errors(logger=crawler_logger)
    def __call__(
        self,
        url: str,
        session: requests.Session,
    ) -> Union[str, None, settings.NotSet]:
        """
        method allows to make request to a given URL with given timeout
        and default values

        :param url: given URL
        :param session: given Session instance
        :return: response content
        :raises appropriate type Error if it happens during runtime
        except for the 404 status error
        """
        response = session.get(url=url, timeout=self._timeout)
        if response.status_code == requests.codes.ok:
            return response.text
        elif response.status_code == requests.codes.not_found:
            return self.default
        else:
            raise HTTPError(f"Crawler could not get data from {url}")


if __name__ == "__main__":
    pass
