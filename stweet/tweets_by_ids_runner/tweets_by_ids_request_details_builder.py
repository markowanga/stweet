"""Prepare params for request in TweetsByIdsRunner."""
from ..http_request import HttpMethod
from ..http_request import RequestDetails

_request_url = 'https://cdn.syndication.twimg.com/tweet'


def get_request_details_for_base_tweet_info(tweet_id: str) -> RequestDetails:
    """Prepare params for request in TweetsByIdsRunner."""
    return RequestDetails(
        http_method=HttpMethod.GET,
        url=_request_url,
        headers=dict(),
        params=dict({'id': tweet_id}),
        timeout=10
    )
