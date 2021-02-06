"""Mapping util."""
import json
from typing import List

from ..model.media import Media

_list_separator = ' , '


def simple_string_list_to_string(values: List[str]) -> str:
    """Method to build string from list."""
    return _list_separator.join(values)


def media_list_to_string(values: List[Media]) -> str:
    """Method to build string from Media list."""
    return json.dumps([it.__dict__() for it in values])


def string_to_simple_string_list(value: str) -> List[str]:
    """Method to build list from specific string."""
    return value.split(_list_separator) if len(value) > 0 else []


def string_to_media_list(value: str) -> List[Media]:
    """Method to build Media list from specific string."""
    parsed_json = json.loads(value)
    return [Media.from_dict(it) for it in parsed_json]
