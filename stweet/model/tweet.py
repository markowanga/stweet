"""Domain Tweet class."""

import json
from dataclasses import dataclass
from typing import Dict, List

_list_separator = ' , '


def _simple_string_list_to_string(values: List[str]) -> str:
    return _list_separator.join(values)


def _string_to_simple_string_list(value: str) -> List[str]:
    return value.split(_list_separator) if len(value) > 0 else []


@dataclass
class Tweet:
    """Domain Tweet class."""

    created_at: str
    id_str: str
    conversation_id_str: str
    full_text: str
    lang: str
    favorited: bool
    retweeted: bool
    retweet_count: int
    favorite_count: int
    reply_count: int
    quote_count: int
    quoted_status_id_str: str
    quoted_status_short_url: str
    quoted_status_expand_url: str
    user_id_str: str
    user_name: str
    user_full_name: str
    user_verified: bool
    in_reply_to_status_id_str: str
    in_reply_to_user_id_str: str
    hashtags: List[str]
    mentions: List[str]
    urls: List[str]

    def to_json_string(self) -> str:
        """Method to prepare json of tweet. Used in JSON serialization."""
        return json.dumps(self, default=lambda o: o.__dict__)

    def to_flat_dict(self):
        """Method to prepare flat dict of tweet. Used in CSV serialization."""
        dictionary = dict(self.__dict__)
        dictionary['hashtags'] = _simple_string_list_to_string(dictionary['hashtags'])
        dictionary['mentions'] = _simple_string_list_to_string(dictionary['mentions'])
        dictionary['urls'] = _simple_string_list_to_string(dictionary['urls'])
        return dictionary

    @staticmethod
    def create_tweet_from_dict(dictionary: Dict[str, any]):
        """Method to create Tweet from dictionary."""
        return Tweet(
            dictionary['created_at'],
            str(dictionary['id_str']),
            str(dictionary['conversation_id_str']),
            dictionary['full_text'],
            dictionary['lang'],
            dictionary['favorited'],
            dictionary['retweeted'],
            dictionary['retweet_count'],
            dictionary['favorite_count'],
            dictionary['reply_count'],
            dictionary['quote_count'],
            dictionary['quoted_status_id_str'],
            dictionary['quoted_status_short_url'],
            dictionary['quoted_status_expand_url'],
            str(dictionary['user_id_str']),
            dictionary['user_name'],
            dictionary['user_full_name'],
            dictionary['user_verified'],
            str(dictionary['in_reply_to_status_id_str']),
            str(dictionary['in_reply_to_user_id_str']),
            dictionary['hashtags'],
            dictionary['mentions'],
            dictionary['urls']
        )

    @staticmethod
    def create_tweet_from_flat_dict(dictionary: Dict[str, any]):
        """Method to create Tweet from flat dictionary."""
        dictionary['hashtags'] = _string_to_simple_string_list(dictionary['hashtags'])
        dictionary['mentions'] = _string_to_simple_string_list(dictionary['mentions'])
        dictionary['urls'] = _string_to_simple_string_list(dictionary['urls'])
        return Tweet.create_tweet_from_dict(dictionary)
