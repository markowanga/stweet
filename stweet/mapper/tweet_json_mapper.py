"""Tweet - json mapper."""
import json

from arrow import Arrow

from .tweet_dict_mapper import create_tweet_from_dict
from ..model import Tweet
from ..model.media import Media


def tweet_to_json(tweet: Tweet) -> str:
    """Method to prepare json of tweet. Used in JSON serialization."""
    return json.dumps(tweet, cls=TweetJsonEncoder)


def create_tweet_from_json(json_value: str) -> Tweet:
    """Method creates tweet from json string."""
    tweet_dict = json.loads(json_value)
    if 'media' not in tweet_dict:
        tweet_dict['media'] = []
    else:
        tweet_dict['media'] = [Media.from_dict(it) for it in tweet_dict['media']]
    return create_tweet_from_dict(tweet_dict)


class TweetJsonEncoder(json.JSONEncoder):
    """JSONEncoder of tweet object."""

    def default(self, obj):
        """Method to convert object to JSON."""
        if isinstance(obj, Arrow):
            return str(obj)
        elif isinstance(obj, Media):
            return obj.__dict__()
        else:
            return obj.__dict__
