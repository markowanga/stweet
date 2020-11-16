from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from model.language import Language


@dataclass(frozen=True)
class SearchTweetsTask:
    simple_search_phrase: Optional[str]
    since: Optional[datetime]
    until: Optional[datetime]
    language: Optional[Language]

    def __init__(
            self,
            simple_search_phrase: Optional[str],
            since: Optional[datetime],
            until: Optional[datetime],
            language: Optional[Language]
    ):
        object.__setattr__(self, 'simple_search_phrase', simple_search_phrase)
        object.__setattr__(self, 'since', since)
        object.__setattr__(self, 'until', until)
        object.__setattr__(self, 'language', language)
