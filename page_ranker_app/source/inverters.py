import multiprocessing
import threading
from abc import ABC, abstractmethod

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from itertools import repeat

from page_ranker_app import settings


class DictionaryInverter(ABC):

    def merge_json(self, base_dict: dict, *args: dict):
        """
        a method to merge arbitrary number of dictionaries according
        to the rules given in task
        :param base_dict:
        :param args: an arbitrary number of dictionaries
        :return: a dictionary
        """
        for dictionary in args:
            for key, value in dictionary.items():
                if key not in base_dict:
                    base_dict[key] = value
                elif type(value) != type(base_dict[key]):
                    raise ValueError(f'Types of values for key {key} '
                                     f'do not match in merged dictionaries')
                elif isinstance(value, list):
                    base_dict[key].extend(value)
                elif isinstance(value, dict):
                    base_dict[key] = self.merge_json(base_dict[key], value)
                else:
                    base_dict[key] = value

    @abstractmethod
    def invert_dict(self, source_dict):
        raise NotImplementedError


class DictionaryInverterSync(DictionaryInverter):

    def invert_dict(self, source_dict):
        """
        The method counts page rank for wiki pages by reversing
        _page_links dictionaries key-value pairs in a way that each
        string from the lists of values becomes a key, and keys of the
        original key-value pairs are put into lists of values for new
        keys and saves results in objects _page_rank dictionary
        :return:
        """
        inverted_dict = {}
        for key, values in source_dict.items():
            for value in values:
                inverted_dict[value] = inverted_dict.get(value, [])
                inverted_dict[value].append(key)
        return inverted_dict


class DictionaryInverterThreading(DictionaryInverter):

    def invert_key_value(self, lock: threading.Lock, result_dict, dictionary: dict, key: str):
        local = threading.local()
        list_of_values = dictionary[key]
        for value in list_of_values:
            local.temp_dict = {value: [key]}
            lock.acquire()
            try:
                self.merge_json(result_dict, local.temp_dict)
            finally:
                lock.release()

    def invert_dict(self, source_dict, max_workers: int = settings.THREADS_INVERTING):
        inverted_dict = {}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            lock = threading.Lock()
            executor.map(
                self.invert_key_value,
                repeat(lock),
                repeat(inverted_dict),
                repeat(source_dict),
                source_dict,
            )
        return inverted_dict


class DictionaryInverterProcessing(DictionaryInverter):

    def invert_key_value(self, lock: multiprocessing.Lock, result_dict, dictionary: dict, key: str):
        list_of_values = dictionary[key]
        for value in list_of_values:
            temp_dict = {value: [key]}
            lock.acquire()
            try:
                self.merge_json(result_dict, temp_dict)
            finally:
                lock.release()

    def invert_dict(self, source_dict, max_workers: int = settings.PROCESSES_INVERTING):
        inverted_dict = {}
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            lock = multiprocessing.Lock()
            executor.map(
                self.invert_key_value,
                repeat(lock),
                repeat(inverted_dict),
                repeat(source_dict),
                source_dict,
            )
        return inverted_dict
