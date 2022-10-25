import multiprocessing
import threading
from abc import ABC, abstractmethod

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from itertools import repeat
from typing import List, Dict

from page_ranker_app import settings


class DictionaryInverter(ABC):
    """
    an interface for dictionary reversing classes
    """
    @staticmethod
    def merge_json(base_dict: Dict, *args: Dict) -> None:
        """
        a method to merge arbitrary number of dictionaries into a base
        dictionary, with special rules that list values for same keys
        are concatenated and if types of values differ, a ValueError
        is raised

        :param base_dict: a base dictionary to merge data in
        :param args: an arbitrary number of dictionaries
        :return: None
        """
        for dictionary in args:
            for key, value in dictionary.items():
                if key not in base_dict:
                    base_dict[key] = value
                elif type(value) != type(base_dict[key]):
                    raise ValueError(
                        f"Types of values for key {key} "
                        f"do not match in merged dictionaries"
                    )
                elif isinstance(value, list):
                    base_dict[key].extend(value)
                else:
                    base_dict[key] = value

    @abstractmethod
    def invert_dict(self, source_dict: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """
        The method inverts dictionaries key-value pairs in a way that
        each string from the lists of values becomes a key, and keys
        of the original key-value pairs are put into lists of values
        for new keys and saves results in objects _page_rank dictionary

        :source_dict: a given dictionary
        :return: an inverted dictionary
        """
        raise NotImplementedError


class DictionaryInverterSync(DictionaryInverter):
    def invert_dict(self, source_dict: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """
        The method inverts all dictionary key-value pairs in a way that
        each string from the lists of values becomes a key, and keys
        of the original key-value pairs are put into lists of values
        for new keys and returns results as a dictionary

        :source_dict: a given dictionary
        :return: an inverted dictionary
        """
        inverted_dict = {}
        for key, values in source_dict.items():
            for value in values:
                inverted_dict[value] = inverted_dict.get(value, [])
                inverted_dict[value].append(key)
        return inverted_dict


class DictionaryInverterThreading(DictionaryInverter):
    def invert_key_value(
        self,
        lock: threading.Lock,
        result_dict: Dict[str, List[str]],
        dictionary: Dict[str, List[str]],
        key: str,
    ) -> None:
        """
        a method that inverts a single dictionary key-value pair
        in a way that each string from the lists of values becomes
        a key, and key of the original key-value pair is put into list
        of values for new keys and merges these reversed pairs in
        a result_dict dictionary
        Uses a lock instance for preventing race conditions
        :param lock:  a lock instance
        :param result_dict: a dictionary
        :param dictionary: an original dictionary
        :param key: a key for getting key-value pair
        :return: None
        """
        local = threading.local()
        list_of_values = dictionary[key]
        for value in list_of_values:
            local.temp_dict = {value: [key]}
            with lock:
                self.merge_json(result_dict, local.temp_dict)

    def invert_dict(
        self,
        source_dict: Dict[str, List[str]],
        max_workers: int = settings.THREADS_INVERTING,
    ) -> Dict[str, List[str]]:
        """
        The method inverts all dictionary key-value pairs in a way that
        each string from the lists of values becomes a key, and keys
        of the original key-value pairs are put into lists of values
        for new keys and returns results as a dictionary
        Uses up to max_workers of active threads

        :param source_dict: a given dictionary
        :param max_workers: a max number of active threads
        :return: an inverted dictionary
        """
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
    def invert_key_value(
        self,
        lock: multiprocessing.Lock,
        result_dict: Dict[str, List[str]],
        dictionary: Dict[str, List[str]],
        key: str,
    ):
        """
        a method that inverts a single dictionary key-value pair
        in a way that each string from the lists of values becomes
        a key, and key of the original key-value pair is put into list
        of values for new keys and merges these reversed pairs in
        a result_dict dictionary
        Uses a lock instance for preventing race conditions
        :param lock:  a lock instance
        :param result_dict: a dictionary
        :param dictionary: an original dictionary
        :param key: a key for getting key-value pair
        :return: None
        """
        list_of_values = dictionary[key]
        for value in list_of_values:
            temp_dict = {value: [key]}
            with lock:
                self.merge_json(result_dict, temp_dict)

    def invert_dict(
        self,
        source_dict: Dict[str, List[str]],
        max_workers: int = settings.PROCESSES_INVERTING,
    ) -> Dict[str, List[str]]:
        """
        The method inverts dictionaries key-value pairs in a way that
        each string from the lists of values becomes a key, and keys
        of the original key-value pairs are put into lists of values
        for new keys and returns results as a dictionary
        Uses up to max_workers of active processes

        :param source_dict: a given dictionary
        :param max_workers: a max number of active processes
        :return: an inverted dictionary
        """
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
