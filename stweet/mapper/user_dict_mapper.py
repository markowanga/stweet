"""User - dict mapper."""
from copy import copy
from typing import Dict

from arrow import get as arrow_get

from .util import simple_string_list_to_string, string_to_simple_string_list
from ..model import User


def user_to_flat_dict(self):
    """Method to prepare flat dict of tweet. Used in CSV serialization."""
    dictionary = dict(self.__dict__)
    dictionary['pinned_tweet_ids_str'] = simple_string_list_to_string(dictionary['pinned_tweet_ids_str'])
    return dictionary


def create_user_from_dict(dictionary: Dict[str, any]):
    """Method to create Tweet from dictionary."""
    return User(
        arrow_get(dictionary['created_at']),
        str(dictionary['id_str']),
        str(dictionary['rest_id_str']),
        dictionary['default_profile'],
        dictionary['default_profile_image'],
        dictionary['description'],
        dictionary['favourites_count'],
        dictionary['followers_count'],
        dictionary['friends_count'],
        dictionary['has_custom_timelines'],
        dictionary['listed_count'],
        dictionary['location'],
        dictionary['media_count'],
        dictionary['name'],
        dictionary['pinned_tweet_ids_str'],
        dictionary['profile_banner_url'],
        dictionary['profile_image_url_https'],
        dictionary['protected'],
        dictionary['screen_name'],
        dictionary['statuses_count'],
        dictionary['verified']
    )


def create_user_from_flat_dict(dictionary: Dict[str, any]) -> User:
    """Method to create Tweet from flat dictionary."""
    dictionary = copy(dictionary)
    dictionary['pinned_tweet_ids_str'] = string_to_simple_string_list(dictionary['pinned_tweet_ids_str'])
    return create_user_from_dict(dictionary)
