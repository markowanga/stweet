"""Runner for get tweets by ids."""
import json
from dataclasses import dataclass
from typing import List, Optional

from .tweets_by_ids_context import TweetsByIdsContext
from .tweets_by_ids_request_details_builder import get_request_details_for_base_tweet_info
from .tweets_by_ids_result import TweetsByIdsResult
from .tweets_by_ids_task import TweetsByIdsTask
from ..auth import AuthTokenProviderFactory, SimpleAuthTokenProviderFactory
from ..http_request import WebClient
from ..http_request.web_client_requests import WebClientRequests
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
            web_client: WebClient = WebClientRequests(),
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
        for tweet_id_to_scrap in self.tweets_by_ids_task.tweet_ids:
            tweet_base_info = self._get_base_tweet_info(tweet_id_to_scrap)
            tweet = self._scrap_full_tweet(tweet_base_info)
            self.tweets_by_ids_context.add_downloaded_tweets_count(1)
            self._process_new_tweets_to_output([tweet])
        return TweetsByIdsResult(self.tweets_by_ids_context.all_download_tweets_count)

    def _get_base_tweet_info(self, tweet_id: str) -> _TweetByIdBaseInfo:
        request_params = get_request_details_for_base_tweet_info(tweet_id)
        request_result = self.web_client.run_request(request_params)
        return self._get_base_tweet_info_from_text_response(tweet_id, request_result.text)

    @staticmethod
    def _get_base_tweet_info_from_text_response(tweet_id: str, response_text: str) -> _TweetByIdBaseInfo:
        parsed_json = json.loads(response_text)
        return _TweetByIdBaseInfo(tweet_id, parsed_json['user']['screen_name'], parsed_json['text'])

    def _scrap_full_tweet(self, tweet_base_info: _TweetByIdBaseInfo) -> Tweet:
        search_tweets_task = SearchTweetsTask(
            exact_words=tweet_base_info.tweet_content,
            from_username=tweet_base_info.username,
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
        return [it for it in tweets_collector.get_scrapped_tweets() if it.id_str == tweet_base_info.id][0]

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
