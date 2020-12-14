"""Mapping util."""
from typing import List

_list_separator = ' , '


def simple_string_list_to_string(values: List[str]) -> str:
    """Method to build string from list."""
    return _list_separator.join(values)


def string_to_simple_string_list(value: str) -> List[str]:
    """Method to build list from specific string."""
    return value.split(_list_separator) if len(value) > 0 else []
