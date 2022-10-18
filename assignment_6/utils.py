import datetime
import requests

from typing import Union

_NOT_SET = object()


class SafeRequest:

    def __init__(self,
                 timeout: Union[datetime.timedelta, float] = 3.0,
                 default=_NOT_SET,
                 ):
        self._timeout = timeout
        self.default = default

    def __call__(self, url: str):
        with requests.Session() as session:
            response = session.get(url=url, timeout=self._timeout)
        if response.status_code == requests.codes.ok:
            return response
        elif response.status_code == requests.codes.not_found:
            return self.default
        else:
            response.raise_for_status()

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, new_value):
        if isinstance(new_value, datetime.timedelta):
            self._timeout = new_value.total_seconds()
        else:
            self._timeout = new_value


if __name__ == '__main__':
    test_url1 = 'https://api.github.com/events'
    getter = SafeRequest(timeout=5)
    resp = getter(url=test_url1)
