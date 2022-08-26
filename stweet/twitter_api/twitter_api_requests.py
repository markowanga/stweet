"""Definitions of all api calls."""
import json
from typing import Optional

from ..http_request.http_method import HttpMethod
from ..http_request.request_details import RequestDetails
from ..model.cursor import Cursor

_default_tweets_count_in_batch = 20


class TwitterApiRequests:
    """Definitions of all api calls."""

    timeout: int

    def __init__(self, timeout: int = 60):
        """Constructor TwitterApiRequests."""
        self.timeout = timeout

    def get_guest_token_request_details(self):
        """Method return request details to get guest token."""
        return RequestDetails(
            HttpMethod.POST,
            'https://api.twitter.com/1.1/guest/activate.json',
            dict(),
            dict(),
            self.timeout
        )

    def get_search_tweet_request_details_new_api(
            self,
            all_download_tweets_count: int,
            cursor: Cursor,
            tweets_limit: Optional[int],
            full_search_query: str
    ) -> RequestDetails:
        count = _default_tweets_count_in_batch \
            if tweets_limit is None \
            else min(_default_tweets_count_in_batch, tweets_limit - all_download_tweets_count)
        params = dict([
            ('include_profile_interstitial_type', '1'),
            ('include_blocking', '1'),
            ('include_blocked_by', '1'),
            ('include_followed_by', '1'),
            ('include_want_retweets', '1'),
            ('include_mute_edge', '1'),
            ('include_can_dm', '1'),
            ('include_can_media_tag', '1'),
            ('skip_status', '1'),
            ('cards_platform', 'Web-12'),
            ('include_cards', '1'),
            ('include_ext_alt_text', 'true'),
            ('include_quote_count', 'true'),
            ('include_reply_count', '1'),
            ('tweet_mode', 'extended'),
            ('include_entities', 'true'),
            ('include_user_entities', 'true'),
            ('include_ext_media_color', 'true'),
            ('include_ext_media_availability', 'true'),
            ('send_error_codes', 'true'),
            ('simple_quoted_tweet', 'true'),
            ('q', full_search_query),
            ('count', count),
            ('query_source', 'typed_query'),
            ('pc', '1'),
            ('spelling_corrections', '1'),
            ('ext', 'mediaStats,highlightedLabel,voiceInfo')
        ])
        if cursor is not None:
            params['cursor'] = cursor.value
        return RequestDetails(
            HttpMethod.GET,
            url='https://twitter.com/i/api/2/search/adaptive.json',
            headers=dict(),
            params=params,
            timeout=self.timeout
        )

    def get_user_details_request_details(self, user_screen_name: str) -> RequestDetails:
        variable_query = {
            "screen_name": user_screen_name,
            "withSafetyModeUserFields": True,
            "withSuperFollowsUserFields": True
        }
        _graphql_token = 'cYsDlVss-qimNYmNlb6inw'  # token generated for ony request in browser
        return RequestDetails(
            http_method=HttpMethod.GET,
            url=f'https://twitter.com/i/api/graphql/{_graphql_token}/UserByScreenName',
            headers=dict(),
            params=dict({
                'variables': json.dumps(variable_query)
            }),
            timeout=self.timeout
        )

    def get_tweet_request_by_id(self, tweet_id: str, cursor: Optional[Cursor]) -> RequestDetails:
        variable_query = {
            "focalTweetId": tweet_id,
            "with_rux_injections": True,
            "includePromotedContent": True,
            "withCommunity": True,
            "withTweetQuoteCount": True,
            "withBirdwatchNotes": True,
            "withSuperFollowsUserFields": True,
            "withUserResults": True,
            "withBirdwatchPivots": True,
            "withReactionsMetadata": True,
            "withReactionsPerspective": True,
            "withSuperFollowsTweetFields": True,
            "withVoice": True
        }
        if cursor is not None:
            variable_query['cursor'] = cursor.value
        _graphql_token = 'kUnCMgMYZCR8GyRZz76IQg'
        return RequestDetails(
            http_method=HttpMethod.GET,
            url=f'https://twitter.com/i/api/graphql/{_graphql_token}/TweetDetail',
            headers=dict(),
            params=dict({
                'variables': json.dumps(variable_query)
            }),
            timeout=self.timeout
        )
