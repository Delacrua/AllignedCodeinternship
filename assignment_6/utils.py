import aiohttp
import asyncio
import datetime
import platform
import requests

from typing import Union


class NotSet:
    pass


_NOT_SET = NotSet()


class SafeRequest:

    def __init__(self,
                 timeout: Union[datetime.timedelta, float] = 3.0,
                 default=_NOT_SET,
                 ):
        self._timeout = timeout
        self.default = default

    def __call__(self, url: str) -> Union[bytes, None, NotSet]:
        with requests.Session() as session:
            response = session.get(url=url, timeout=self._timeout)
        if response.status_code == requests.codes.ok:
            return response.content
        elif response.status_code == requests.codes.not_found:
            return self.default
        else:
            response.raise_for_status()

    async def invoke(self, url: str) -> Union[bytes, None, NotSet]:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                if response.status == requests.codes.ok:
                    response_data = await response.read()
                    return response_data
                elif response.status == requests.codes.not_found:
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
    test_url1 = 'https://en.wikipedia.org/wiki/Agostino_Cornacchini'
    getter = SafeRequest(timeout=5)
    resp = getter(url=test_url1)
    print(resp)

    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    resp = asyncio.run(getter.invoke(test_url1))
    print(resp)
