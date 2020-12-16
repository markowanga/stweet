"""Tweet - json mapper."""
import json

from arrow import Arrow

from .tweet_dict_mapper import create_tweet_from_dict
from ..model import Tweet


def tweet_to_json(tweet: Tweet) -> str:
    """Method to prepare json of tweet. Used in JSON serialization."""
    return json.dumps(tweet, default=lambda o: str(o) if isinstance(o, Arrow) else o.__dict__)


def create_tweet_from_json(json_value: str) -> Tweet:
    """Method creates tweet from json string."""
    tweet_dict = json.loads(json_value)
    return create_tweet_from_dict(tweet_dict)
