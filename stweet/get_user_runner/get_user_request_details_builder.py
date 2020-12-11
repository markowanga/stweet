"""Prepare params for request in TweetsByIdsRunner."""
import json

from .get_user_context import GetUserContext
from ..http_request import HttpMethod
from ..http_request import RequestDetails

_graphql_token = 'esn6mjj-y68fNAj45x5IYA'
_request_url = f'https://api.twitter.com/graphql/{_graphql_token}/UserByScreenName'


def get_user_details_request_details(username: str, get_user_context: GetUserContext) -> RequestDetails:
    """Prepare params for request in TweetsByIdsRunner."""
    return RequestDetails(
        http_method=HttpMethod.GET,
        url=_request_url + f"?variables=%7B%22screen_name%22%3A%22{username}%22%2C%22withHighlightedLabel%22%3Atrue%7D",
        headers=dict({
            'x-guest-token': get_user_context.guest_auth_token,
            'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
        }),
        params=dict({
            # 'variables': _get_variables_string(username)
        }),
        timeout=10
    )


def _get_variables_string(username: str) -> str:
    return json.dumps({'screen_name': username, 'withHighlightedLabel': True})
