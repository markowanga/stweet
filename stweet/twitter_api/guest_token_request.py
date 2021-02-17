import json

from ..http_request import RequestDetails, HttpMethod
from ..search_runner import SearchRunContext
from ..search_runner.search_tweets_task import SearchTweetsTask

_default_tweets_count_in_batch = 100


class TwitterApi:
    timeout: int

    def __init__(self, timeout: int = 20):
        self.timeout = timeout

    def get_guest_token(self):
        return RequestDetails(
            HttpMethod.POST,
            'https://api.twitter.com/1.1/guest/activate.json',
            dict(),
            dict(),
            self.timeout
        )

    def get_search_tweet_request_details(
            self,
            search_run_context: SearchRunContext,
            search_tweets_task: SearchTweetsTask
    ) -> RequestDetails:
        """Returns the RequestDetails for simple request for tweets."""
        return RequestDetails(
            HttpMethod.GET,
            url='https://api.twitter.com/2/search/adaptive.json',
            headers=dict(),
            params=dict([
                ('include_can_media_tag', '1'),
                ('include_ext_alt_text', 'true'),
                ('include_quote_count', 'true'),
                ('include_reply_count', '1'),
                ('tweet_mode', 'extended'),
                ('include_entities', 'true'),
                ('include_user_entities', 'true'),
                ('include_ext_media_availability', 'true'),
                ('send_error_codes', 'true'),
                ('simple_quoted_tweet', 'true'),
                ('count', _default_tweets_count_in_batch \
                    if search_tweets_task.tweets_limit is None \
                    else min(_default_tweets_count_in_batch,
                             search_tweets_task.tweets_limit - search_run_context.all_download_tweets_count)),
                ('cursor', search_run_context.scroll_token),
                ('spelling_corrections', '1'),
                ('ext', 'mediaStats%2ChighlightedLabel'),
                ('tweet_search_mode', 'live'),
                ('f', 'tweets'),  # if not config.Popular_tweets
                ('q', search_tweets_task.get_full_search_query())
            ]),
            timeout=self.timeout
        )

    def get_request_details_for_base_tweet_info(self, tweet_id: str) -> RequestDetails:
        """Prepare params for request in TweetsByIdsRunner."""
        return RequestDetails(
            http_method=HttpMethod.GET,
            url='https://cdn.syndication.twimg.com/tweet',
            headers=dict(),
            params=dict({'id': tweet_id}),
            timeout=self.timeout
        )

    def get_user_details_request_details(self, username: str) -> RequestDetails:
        """Prepare params for request in TweetsByIdsRunner."""
        _graphql_token = 'esn6mjj-y68fNAj45x5IYA'  # token generated for ony request in browser
        return RequestDetails(
            http_method=HttpMethod.GET,
            url=f'https://api.twitter.com/graphql/{_graphql_token}/UserByScreenName',
            headers=dict(),
            params=dict({
                'variables': json.dumps({'screen_name': username, 'withHighlightedLabel': True})
            }),
            timeout=self.timeout
        )
