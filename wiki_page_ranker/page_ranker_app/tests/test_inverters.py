import pytest
from typing import Dict, Tuple, List

from page_ranker_app.source import inverters


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            ({"a": ["url1", "url2"], "b": ["url3"]}, {"c": ["url4"]}),
            {"a": ["url1", "url2"], "b": ["url3"], "c": ["url4"]},
        ),
        (
            (
                {"a": ["url1", "url2"], "b": ["url3"]},
                {"b": ["url5"], "c": ["url4"]},
            ),
            {"a": ["url1", "url2"], "b": ["url3", "url5"], "c": ["url4"]},
        ),
    ],
)
def test_merge_json(test_input: Tuple[Dict], expected: Dict):
    inverter = inverters.DictionaryInverterThreading()
    base_dict, *args = test_input
    inverter.merge_json(base_dict, *args)
    assert base_dict == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            (
                {"a": ["url1", "url2"], "b": ["url3"]},
                {"b": "url5", "c": ["url4"]},
            ),
            {"a": ["url1", "url2"], "b": ["url3", "url5"], "c": ["url4"]},
        ),
        (
            (
                {"a": ["url1", "url2"], "b": ["url3"]},
                {"b": 5, "c": ["url4"]},
            ),
            {"a": ["url1", "url2"], "b": ["url3", "url5"], "c": ["url4"]},
        ),
    ],
)
def test_merge_json_value_error(test_input: Tuple[Dict], expected: Dict):
    inverter = inverters.DictionaryInverterThreading()
    base_dict, *args = test_input
    with pytest.raises(ValueError):
        inverter.merge_json(base_dict, *args)


inverting_assets = [
    (
        {"a": ["url1"], "b": ["url3", "url5"], "c": ["url4"]},
        {"url1": ["a"], "url3": ["b"], "url5": ["b"], "url4": ["c"]},
    ),
    (
        {"a": ["url1", "url2"], "b": ["url3", "url4"], "c": ["url4"]},
        {"url1": ["a"], "url2": ["a"], "url3": ["b"], "url4": ["b", "c"]},
    ),
]


@pytest.mark.parametrize("source_dict, expected", inverting_assets)
def test_invert_dict_sync(
    source_dict: Dict[str, List[str]], expected: Dict[str, List[str]]
):
    inverter = inverters.DictionaryInverterSync()
    assert inverter.invert_dict(source_dict) == expected


@pytest.mark.parametrize("source_dict, expected", inverting_assets)
def test_invert_dict_threaded(
    source_dict: Dict[str, List[str]], expected: Dict[str, List[str]]
):
    inverter = inverters.DictionaryInverterThreading()
    assert inverter.invert_dict(source_dict) == expected
