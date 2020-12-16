"""User - json mapper."""
import json

from arrow import Arrow

from .user_dict_mapper import create_user_from_dict
from ..model import User


def user_to_json(user: User) -> str:
    """Method to prepare json of user. Used in JSON serialization."""
    return json.dumps(user, default=lambda o: str(o) if isinstance(o, Arrow) else o.__dict__)


def create_user_from_json(json_value: str) -> User:
    """Creates user from json string."""
    tweet_dict = json.loads(json_value)
    return create_user_from_dict(tweet_dict)
