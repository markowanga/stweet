"""Prepare params for request in TweetsByIdsRunner."""
import json

from .get_users_context import GetUsersContext
from ..http_request import HttpMethod
from ..http_request import RequestDetails

_graphql_token = 'esn6mjj-y68fNAj45x5IYA'
_request_url = f'https://api.twitter.com/graphql/{_graphql_token}/UserByScreenName'

_auth_token = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4p' \
              'uTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'


def get_user_details_request_details(username: str, get_user_context: GetUsersContext) -> RequestDetails:
    """Prepare params for request in TweetsByIdsRunner."""
    return RequestDetails(
        http_method=HttpMethod.GET,
        url=_request_url,
        headers=dict({
            'x-guest-token': get_user_context.guest_auth_token,
            'Authorization': _auth_token
        }),
        params=dict({
            'variables': _get_variables_string(username)
        }),
        timeout=10
    )


def _get_variables_string(username: str) -> str:
    return json.dumps({'screen_name': username, 'withHighlightedLabel': True})
