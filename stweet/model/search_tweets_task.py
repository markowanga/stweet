"""Domain SearchTweetsTask class."""

from dataclasses import dataclass
from typing import Optional

from arrow import Arrow

from .language import Language
from .replies_filter import RepliesFilter


def _format_date(arrow_time: Arrow) -> int:
    print('arrow_time ' + str(arrow_time))
    return arrow_time.int_timestamp


@dataclass(frozen=True)
class SearchTweetsTask:
    """Domain SearchTweetsTask class."""

    all_words: Optional[str]
    exact_words: Optional[str]
    any_word: Optional[str]
    from_username: Optional[str]
    to_username: Optional[str]
    since: Optional[Arrow]
    until: Optional[Arrow]
    language: Optional[Language]
    tweets_count: Optional[int]
    replies_filter: Optional[RepliesFilter]

    def __init__(
            self,
            all_words: Optional[str] = None,
            exact_words: Optional[str] = None,
            any_word: Optional[str] = None,
            from_username: Optional[str] = None,
            to_username: Optional[str] = None,
            since: Optional[Arrow] = None,
            until: Optional[Arrow] = None,
            language: Optional[Language] = None,
            tweets_count: Optional[int] = None,
            replies_filter: Optional[RepliesFilter] = None
    ):
        """Class constructor."""
        object.__setattr__(self, 'all_words', all_words)
        object.__setattr__(self, 'exact_words', exact_words)
        object.__setattr__(self, 'any_word', any_word)
        object.__setattr__(self, 'from_username', from_username)
        object.__setattr__(self, 'to_username', to_username)
        object.__setattr__(self, 'since', since)
        object.__setattr__(self, 'until', until)
        object.__setattr__(self, 'language', language)
        object.__setattr__(self, 'tweets_count', tweets_count)
        object.__setattr__(self, 'replies_filter', replies_filter)
        return

    def get_full_search_query(self) -> str:
        """Method to return full search query."""
        query = ''
        if self.all_words is not None:
            query += self.all_words
        if self.exact_words is not None:
            query += f' "{self.exact_words}"'
        if self.any_word is not None:
            query += f' ({" OR ".join(self.any_word.split(" "))})'
        if self.language is not None:
            query += f' lang:{self.language.short_value}'
        if self.from_username:
            query += f' from:{self.from_username}'
        if self.since is not None:
            query += f" since:{_format_date(self.since)}"
        if self.until is not None:
            query += f" until:{_format_date(self.until)}"
        if self.to_username:
            query += f" to:{self.to_username}"
        if self.replies_filter is not None:
            if self.replies_filter == RepliesFilter.ONLY_REPLIES:
                query += " filter:replies"
            elif self.replies_filter == RepliesFilter.ONLY_ORIGINAL:
                query += " -filter:replies"
        return query
