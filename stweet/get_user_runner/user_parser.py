"""Parser of JSON string to User."""
import json
from typing import List

from arrow import Arrow
from dateutil import parser

from ..exceptions.user_suspended_exception import UserSuspendedException
from ..model import User


def _get_error_codes(parsed_response: any) -> List[int]:
    return [it['code'] for it in parsed_response['errors'] if 'code' in it]


def _is_user_suspended(parsed_response: any) -> bool:
    if 'errors' not in parsed_response:
        return False
    error_codes = _get_error_codes(parsed_response)
    return any(error_code == 63 for error_code in error_codes)


def _get_user_urls(legacy_user_json: any) -> List[str]:
    try:
        urls = legacy_user_json['entities']['url']['urls']
        return [it['expanded_url'] for it in urls]
    except KeyError:
        return []


def parse_user(response_content: str) -> User:
    """Parser of JSON string to User."""
    parsed_response = json.loads(response_content)
    if _is_user_suspended(parsed_response):
        raise UserSuspendedException()
    user_json = parsed_response['data']['user']
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
        verified=legacy_user_json['verified'],
        urls=_get_user_urls(legacy_user_json)
    )
