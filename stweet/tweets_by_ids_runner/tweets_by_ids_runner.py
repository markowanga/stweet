"""Runner for get tweets by ids."""
import json
from dataclasses import dataclass
from typing import List, Optional

from arrow import Arrow, get as arrow_get

from stweet.http_request.requests.requests_web_client import RequestsWebClient
from .tweets_by_ids_context import TweetsByIdsContext
from .tweets_by_ids_request_details_builder import get_request_details_for_base_tweet_info
from .tweets_by_ids_result import TweetsByIdsResult
from .tweets_by_ids_task import TweetsByIdsTask
from ..auth import AuthTokenProviderFactory, SimpleAuthTokenProviderFactory
from ..http_request import WebClient
from ..model import Tweet
from ..search_runner import TweetSearchRunner
from ..search_runner.parse import BaseTweetParser
from ..search_runner.parse import TweetParser
from ..search_runner.search_run_context import SearchRunContext
from ..search_runner.search_tweets_task import SearchTweetsTask
from ..tweet_output import TweetOutput, CollectorTweetOutput


@dataclass
class _TweetByIdBaseInfo:
    id: str
    username: str
    tweet_content: str
    created_at: Arrow


class TweetsByIdsRunner:
    """Runner class to process task to search tweets."""

    tweets_by_ids_context: TweetsByIdsContext
    tweets_by_ids_task: TweetsByIdsTask
    tweet_outputs: List[TweetOutput]
    web_client: WebClient
    tweet_parser: TweetParser
    auth_token_provider_factory: AuthTokenProviderFactory

    def __init__(
            self,
            tweets_by_ids_task: TweetsByIdsTask,
            tweet_outputs: List[TweetOutput],
            tweets_by_ids_context: Optional[TweetsByIdsContext] = None,
            web_client: WebClient = RequestsWebClient(),
            tweet_parser: TweetParser = BaseTweetParser(),
            auth_token_provider_factory: AuthTokenProviderFactory = SimpleAuthTokenProviderFactory()
    ):
        """Constructor to create object."""
        self.tweets_by_ids_context = TweetsByIdsContext() if tweets_by_ids_context is None else tweets_by_ids_context
        self.tweets_by_ids_task = tweets_by_ids_task
        self.tweet_outputs = tweet_outputs
        self.web_client = web_client
        self.tweet_parser = tweet_parser
        self.auth_token_provider_factory = auth_token_provider_factory
        return

    def run(self) -> TweetsByIdsResult:
        """Main search_runner method."""
        self._prepare_token()
        tweet_ids_not_scrapped = []
        for tweet_id_to_scrap in self.tweets_by_ids_task.tweet_ids:
            tweet_base_info = self._get_base_tweet_info(tweet_id_to_scrap)
            if tweet_base_info is None:
                tweet_ids_not_scrapped.append(tweet_id_to_scrap)
            else:
                tweet = self._scrap_full_tweet(tweet_base_info)
                if tweet is None:
                    tweet_ids_not_scrapped.append(tweet_id_to_scrap)
                else:
                    self.tweets_by_ids_context.add_downloaded_tweets_count(1)
                    self._process_new_tweets_to_output([tweet])
        return TweetsByIdsResult(self.tweets_by_ids_context.all_download_tweets_count, tweet_ids_not_scrapped)

    def _get_base_tweet_info(self, tweet_id: str) -> Optional[_TweetByIdBaseInfo]:
        request_params = get_request_details_for_base_tweet_info(tweet_id)
        request_result = self.web_client.run_request(request_params)
        return self._get_base_tweet_info_from_text_response(tweet_id, request_result.text) \
            if request_result.is_success() \
            else None

    @staticmethod
    def _get_base_tweet_info_from_text_response(tweet_id: str, response_text: str) -> Optional[_TweetByIdBaseInfo]:
        parsed_json = json.loads(response_text)
        return _TweetByIdBaseInfo(
            tweet_id,
            parsed_json['user']['screen_name'],
            parsed_json['text'],
            arrow_get(parsed_json['created_at'])
        )

    def _scrap_full_tweet(self, tweet_base_info: _TweetByIdBaseInfo) -> Optional[Tweet]:
        search_tweets_task = SearchTweetsTask(
            from_username=tweet_base_info.username,
            since=tweet_base_info.created_at.shift(minutes=-1),
            until=tweet_base_info.created_at.shift(minutes=1)
        )
        tweets_collector = CollectorTweetOutput()
        search_context = SearchRunContext(guest_auth_token=self.tweets_by_ids_context.guest_auth_token)
        TweetSearchRunner(
            search_tweets_task=search_tweets_task,
            tweet_outputs=[tweets_collector],
            web_client=self.web_client,
            search_run_context=search_context,
            tweet_parser=self.tweet_parser,
            auth_token_provider_factory=self.auth_token_provider_factory
        ).run()
        self.tweets_by_ids_context.guest_auth_token = search_context.guest_auth_token
        filtered_list = [it for it in tweets_collector.get_scrapped_tweets() if it.id_str == tweet_base_info.id]
        return filtered_list[0] if len(filtered_list) > 0 else None

    def _refresh_token(self):
        token_provider = self.auth_token_provider_factory.create(self.web_client)
        self.tweets_by_ids_context.guest_auth_token = token_provider.get_new_token()
        return

    def _prepare_token(self):
        if self.tweets_by_ids_context.guest_auth_token is None:
            self._refresh_token()
        return

    def _process_new_tweets_to_output(self, new_tweets: List[Tweet]):
        for tweet_output in self.tweet_outputs:
            tweet_output.export_tweets(new_tweets)
        return
