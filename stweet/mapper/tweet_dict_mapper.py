"""Tweet - dict mapper."""
from copy import copy
from typing import Dict

from arrow import get as arrow_get

from .util import simple_string_list_to_string, string_to_simple_string_list
from ..model import Tweet


def tweet_to_flat_dict(self):
    """Method to prepare flat dict of tweet. Used in CSV serialization."""
    dictionary = dict(self.__dict__)
    dictionary['hashtags'] = simple_string_list_to_string(dictionary['hashtags'])
    dictionary['mentions'] = simple_string_list_to_string(dictionary['mentions'])
    dictionary['urls'] = simple_string_list_to_string(dictionary['urls'])
    return dictionary


def create_tweet_from_dict(dictionary: Dict[str, any]):
    """Method to create Tweet from dictionary."""
    return Tweet(
        arrow_get(dictionary['created_at']),
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


def create_tweet_from_flat_dict(dictionary: Dict[str, any]) -> Tweet:
    """Method to create Tweet from flat dictionary."""
    dictionary = copy(dictionary)
    dictionary['hashtags'] = string_to_simple_string_list(dictionary['hashtags'])
    dictionary['mentions'] = string_to_simple_string_list(dictionary['mentions'])
    dictionary['urls'] = string_to_simple_string_list(dictionary['urls'])
    return create_tweet_from_dict(dictionary)
