from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from stweet.model.language import Language


@dataclass(frozen=True)
class SearchTweetsTask:
    simple_search_phrase: Optional[str]
    from_username: Optional[str]
    to_username: Optional[str]
    since: Optional[datetime]
    until: Optional[datetime]
    language: Optional[Language]
    verified_user: bool

    def __init__(
            self,
            simple_search_phrase: Optional[str],
            from_username: Optional[str],
            to_username: Optional[str],
            since: Optional[datetime],
            until: Optional[datetime],
            language: Optional[Language]
    ):
        object.__setattr__(self, 'simple_search_phrase', simple_search_phrase)
        object.__setattr__(self, 'from_username', from_username)
        object.__setattr__(self, 'to_username', to_username)
        object.__setattr__(self, 'since', since)
        object.__setattr__(self, 'until', until)
        object.__setattr__(self, 'language', language)
        return

    def get_full_search_query(self) -> str:
        query = self.simple_search_phrase
        if self.language is not None:
            query += f' lang:{self.language.short_value}'
        if self.from_username:
            query += f' from:{self.from_username}'
        if self.since is not None:
            query += f" since:{self._format_date(self.since)}"
        if self.until is not None:
            query += f" until:{self._format_date(self.until)}"
        # if self.verified_user is True:  # TODO check it works
        #     query += " filter:verified"
        if self.to_username:
            query += f" to:{self.to_username}"  # TODO check it works
        # if config.Replies:
        #     q += " filter:replies"
        #     # although this filter can still be used, but I found it broken in my preliminary
        #     # testing, needs more testing
        # if config.Native_retweets:
        #     q += " filter:nativeretweets"
        # if config.Min_likes:
        #     q += f" min_faves:{config.Min_likes}"
        # if config.Min_retweets:
        #     q += f" min_retweets:{config.Min_retweets}"
        # if config.Min_replies:
        #     q += f" min_replies:{config.Min_replies}"
        # if config.Links == "include":
        #     q += " filter:links"
        # elif config.Links == "exclude":
        #     q += " exclude:links"
        # if config.Source:
        #     q += f" source:\"{config.Source}\""
        # if config.Members_list:
        #     q += f" list:{config.Members_list}"
        # if config.Filter_retweets:
        #     q += f" exclude:nativeretweets exclude:retweets"
        # if config.Custom_query:
        #     q = config.Custom_query
        return query

    @staticmethod
    def _format_date(date) -> int:
        try:
            return int(datetime.strptime(date, "%Y-%m-%d %H:%M:%S").timestamp())
        except ValueError:
            return int(datetime.strptime(date, "%Y-%m-%d").timestamp())
