"""Domain Media class used to store media in Tweet."""
from dataclasses import dataclass
from typing import Dict

_URL = 'url'
_TYPE = 'type'


@dataclass
class Media:
    """Domain Media class used to store media in Tweet."""

    url: str
    type: str

    @classmethod
    def from_dict(cls, dictionary: Dict[str, str]):
        """Method to create Media class from dict."""
        return cls(dictionary[_URL], dictionary[_TYPE])

    def __dict__(self) -> Dict[str, str]:
        """Convert Media object to dictionary."""
        return dict({
            _URL: self.url,
            _TYPE: self.type
        })
