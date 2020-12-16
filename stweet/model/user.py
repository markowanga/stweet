"""Domain User class."""

from dataclasses import dataclass
from typing import List

from arrow import Arrow


@dataclass
class User:
    """Domain User class."""

    created_at: Arrow
    id_str: str
    rest_id_str: str
    default_profile: bool
    default_profile_image: bool
    description: str
    favourites_count: int
    followers_count: int
    friends_count: int
    has_custom_timelines: bool
    listed_count: int
    location: str
    media_count: str
    name: str
    pinned_tweet_ids_str: List[str]
    profile_banner_url: str
    profile_image_url_https: str
    protected: bool
    screen_name: str
    statuses_count: int
    verified: bool
