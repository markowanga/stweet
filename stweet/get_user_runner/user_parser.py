"""Parser of JSON string to User."""
import json

from arrow import Arrow
from dateutil import parser

from ..model import User


def parse_user(response_content: str) -> User:
    """Parser of JSON string to User."""
    user_json = json.loads(response_content)['data']['user']
    legacy_user_json = user_json['legacy']
    return User(
        created_at=Arrow.fromdatetime(parser.parse(legacy_user_json['created_at'])),
        id_str=user_json['id'],
        rest_id_str=user_json['rest_id'],
        default_profile=legacy_user_json['default_profile'],
        default_profile_image=legacy_user_json['default_profile_image'],
        description=legacy_user_json['description'],
        favourites_count=legacy_user_json['favourites_count'],
        followers_count=legacy_user_json['favourites_count'],
        friends_count=legacy_user_json['friends_count'],
        has_custom_timelines=legacy_user_json['has_custom_timelines'],
        listed_count=legacy_user_json['listed_count'],
        location=legacy_user_json['location'],
        media_count=legacy_user_json['media_count'],
        name=legacy_user_json['name'],
        pinned_tweet_ids_str=legacy_user_json['pinned_tweet_ids_str'],
        profile_banner_url=legacy_user_json['profile_banner_url'] if 'profile_banner_url' in legacy_user_json else '',
        profile_image_url_https=legacy_user_json['profile_image_url_https'],
        protected=legacy_user_json['protected'],
        screen_name=legacy_user_json['screen_name'],
        statuses_count=legacy_user_json['statuses_count'],
        verified=legacy_user_json['verified']
    )
