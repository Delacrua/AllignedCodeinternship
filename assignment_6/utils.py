import aiofiles
import aiohttp
import asyncio
import datetime
import hashlib
import os
import platform
import requests
import timeit

from aiofiles import os as async_os
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from typing import Union


class timer:
    """
    a context manager for measuring of time used for a code block
    to operate and printing it to stdout
    """
    def __enter__(self):
        self.start = timeit.default_timer()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = timeit.default_timer()
        print(f'Code block took {(self.end - self.start):.5f} seconds '
              f'to operate')


class NotSet:
    pass


_NOT_SET = NotSet()


class SafeRequest:
    """
    a callable class that allows making requests to a URL
    """
    def __init__(self,
                 timeout: Union[datetime.timedelta, float] = 3.0,
                 default=_NOT_SET,
                 ):
        """
        object constructor, utilizing a property for value validation
        and conversion
        :param timeout: a timeout for making a request in seconds
        :param default: a default value for whenever a request fails
        with 404 status
        """
        self._timeout = timeout
        self.default = default

    def __call__(self, url: str) -> Union[bytes, None, NotSet]:
        """
        method allows to make request to a given URL with given timeout
        and default values
        :param url: given URL
        :return: response content
        :raises appropriate type Error if it happens during runtime
        except for the 404 status error
        """
        with requests.Session() as session:
            response = session.get(url=url, timeout=self._timeout)
        if response.status_code == requests.codes.ok:
            return response.content
        elif response.status_code == requests.codes.not_found:
            return self.default
        else:
            response.raise_for_status()

    async def invoke(self, url: str) -> Union[bytes, None, NotSet]:
        """
        method allows to asynchronously make request to a given URL with
        given timeout and default values
        :param url: given URL
        :return: response content
        :raises appropriate type Error if it happens during runtime
        except for the 404 status error
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, timeout=self._timeout) as response:
                if response.status == requests.codes.ok:
                    response_data = await response.read()
                    return response_data
                elif response.status == requests.codes.not_found:
                    return self.default
                else:
                    response.raise_for_status()

    @property
    def timeout(self):
        """
        getter for timeout attribute
        :return: timeout attribute
        """
        return self._timeout

    @timeout.setter
    def timeout(self, new_value: Union[datetime.timedelta, float]):
        """
        setter for timeout attribute
        :param new_value: new value for timeout attribute
        :return: None
        """
        if isinstance(new_value, datetime.timedelta):
            self._timeout = new_value.total_seconds()
        else:
            self._timeout = new_value


def get_file_dict(start_path: str = '.') -> dict[str: NotSet]:
    """
    Function makes a run on all files in a given directory and nested
    directories and makes a dict of filepaths for further processing
    :param start_path: given starting directory
    :return:
    """
    seen = {}
    for root_dir, cur_dir, files in os.walk(start_path):
        for file_name in files:
            filepath = os.path.join(root_dir, file_name)
            seen[filepath] = _NOT_SET
    return seen


def get_file_size(
        files_dict: dict[str: NotSet],
        filepath: str,
) -> None:
    """
    Function checks file size for a given filepath and writes results
    to the given dictionary
    :param files_dict: given dictionary
    :param filepath: given filepath
    :return: None
    """
    try:
        stat = os.stat(filepath)
    except OSError:
        pass
    else:
        files_dict[filepath] = stat.st_size


def get_file_hash(
        files_dict: dict[str: Union[NotSet, int]],
        filepath: str,
) -> None:
    """
    Function counts a hashsum of file contents for a given filepath and
    writes results to the given dictionary
    :param files_dict: given dictionary
    :param filepath: given filepath
    :return: None
    """
    file_sha = hashlib.sha1()
    try:
        with open(filepath, 'rb') as file_bytes_object:
            while True:
                buffer = file_bytes_object.read(4096)
                if not buffer:
                    break
                file_sha.update(buffer)
    except Exception:
        pass
    finally:
        files_dict[filepath] = (files_dict[filepath], file_sha.hexdigest())


def calculate_stats(start_path: str) -> namedtuple:
    """
    The function counts statistics for a given directory path returning
    a namedtuple 'Stats' with fields ('total_files', 'total_size',
    'check_sum') which contain total number of files in directory and
    nested directories, their total size in kb and a hashsum counted
    in such way that any change of files or directories names or content
    will result in hashsum change
    Uses threading for optimizing speed on IO-bound processes
    :param start_path: given starting directory
    :return: namedtuple
    """
    stats = namedtuple('Stats', ('total_files', 'total_size', 'check_sum'))
    _sha_hash = hashlib.sha1()
    _files_dict = get_file_dict(start_path)

    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(get_file_size, repeat(_files_dict), _files_dict.keys())

    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(get_file_hash, repeat(_files_dict), _files_dict.keys())

    _files_dict: dict[str: tuple[Union[NotSet, int], str]]
    _files_dict = {key: value for key, value in _files_dict.items()
                   if value[0] is not _NOT_SET}

    for filepath, value in _files_dict.items():
        _sha_hash.update(filepath.encode('utf-8'))
        _sha_hash.update(value[1].encode('utf-8'))

    return stats(
        len(_files_dict),
        sum(values[0] for values in _files_dict.values()),
        _sha_hash.hexdigest(),
    )


async def get_file_size_async(
        files_dict: dict[str: NotSet],
        filepath: str,
        semaphore: asyncio.Semaphore,
) -> None:
    """
    Function checks file size for a given filepath and  writes results
    to the given dictionary using a Semaphore object to prevent errors
    caused by too many files opened
    :param files_dict: given dictionary
    :param filepath: given filepath
    :param semaphore: given Semaphore object
    :return: None
    """
    async with semaphore:
        try:
            stat = await async_os.stat(filepath)
        except OSError:
            pass
        else:
            files_dict[filepath] = stat.st_size


async def get_file_hash_async(
        files_dict: dict[str: Union[NotSet, int]],
        filepath: str,
        semaphore: asyncio.Semaphore,
) -> None:
    """
    Function counts a hashsum of file contents for a given filepath and
    writes results to the given dictionary using a Semaphore object
    to prevent errors caused by too many files opened
    :param files_dict: given dictionary
    :param filepath: given filepath
    :param semaphore: given Semaphore object
    :return: None
    """
    file_sha = hashlib.sha1()
    try:
        async with aiofiles.open(filepath, 'rb') as file_bytes_object, \
                semaphore:
            while True:
                buffer = await file_bytes_object.read(4096)
                if not buffer:
                    break
                file_sha.update(buffer)
    except Exception:
        pass
    finally:
        files_dict[filepath] = (files_dict[filepath], file_sha.hexdigest())


async def calculate_stats_async(start_path: str):
    """
    The function counts statistics for a given directory path returning
    a namedtuple 'Stats' with fields ('total_files', 'total_size',
    'check_sum') which contain total number of files in directory and
    nested directories, their total size in kb and a hashsum counted
    in such way that any change of files or directories names or content
    will result in hashsum change
    Uses asyncio for optimizing speed on IO-bound processes
    :param start_path: given starting directory
    :return: namedtuple
    """
    stats = namedtuple('Stats', ('total_files', 'total_size', 'check_sum'))
    sema = asyncio.Semaphore(100)
    _sha_hash = hashlib.sha1()
    _files_dict = get_file_dict(start_path)

    await asyncio.gather(*[get_file_size_async(_files_dict, filepath, sema)
                           for filepath in _files_dict])
    await asyncio.gather(*[get_file_hash_async(_files_dict, filepath, sema)
                           for filepath in _files_dict])

    _files_dict: dict[str: tuple[Union[NotSet, int], str]]
    _files_dict = {key: value for key, value in _files_dict.items()
                   if value[0] is not _NOT_SET}

    for filepath, values in _files_dict.items():
        _sha_hash.update(filepath.encode('utf-8'))
        _sha_hash.update(values[1].encode('utf-8'))

    return stats(
        len(_files_dict),
        sum(values[0] for values in _files_dict.values()),
        _sha_hash.hexdigest(),
    )


if __name__ == '__main__':
    print('-----> SafeRequest block <-----')
    test_url1 = 'https://en.wikipedia.org/wiki/Agostino_Cornacchini'
    getter = SafeRequest(timeout=5)
    resp = getter(url=test_url1)
    print(resp)

    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    resp = asyncio.run(getter.invoke(test_url1))
    print(resp)

    test_directory = r'D:\PycharmProjects\DRFTutorial'
    print('-----> Threading block <-----')
    with timer():
        print(calculate_stats(test_directory))
    print('-----> Asyncio block <-----')
    with timer():
        print(asyncio.run(calculate_stats_async(test_directory)))
