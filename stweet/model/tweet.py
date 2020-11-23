"""Domain Tweet class."""

import json
from dataclasses import dataclass
from typing import Dict


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

    def to_json_string(self) -> str:
        """Method to prepare json of tweet. Used in JSON serialization."""
        return json.dumps(self, default=lambda o: o.__dict__)

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
            str(dictionary['in_reply_to_user_id_str'])
        )
