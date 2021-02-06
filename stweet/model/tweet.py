"""Domain Tweet class."""

from dataclasses import dataclass
from typing import List

from arrow import Arrow

from .media import Media


@dataclass
class Tweet:
    """Domain Tweet class."""

    created_at: Arrow
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
    media: List[Media]
    hashtags: List[str]
    mentions: List[str]
    urls: List[str]
