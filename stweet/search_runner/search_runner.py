"""Runner to process task to search tweets."""
import json
from typing import List, Optional

from ..exceptions.scrap_batch_bad_response import ScrapBatchBadResponse
from ..http_request.request_details import RequestDetails
from ..http_request.web_client import WebClient
from ..model.tweet_raw import TweetRaw
from ..model.user_raw import UserRaw
from ..raw_output.raw_data_output import RawDataOutput
from ..twitter_api.default_twitter_web_client_provider import \
    DefaultTwitterWebClientProvider
from ..twitter_api.twitter_api_requests import TwitterApiRequests
from .search_run_context import SearchRunContext
from .search_tweets_result import SearchTweetsResult
from .search_tweets_task import SearchTweetsTask
from .tweet_raw_parser import get_scroll_cursor, parse_tweets, parse_users


class TweetSearchRunner:
    """Runner class to process task to search tweets."""

    search_run_context: SearchRunContext
    search_tweets_task: SearchTweetsTask
    tweet_raw_data_outputs: List[RawDataOutput]
    user_raw_data_outputs: List[RawDataOutput]
    web_client: WebClient

    def __init__(
            self,
            search_tweets_task: SearchTweetsTask,
            tweet_raw_data_outputs: List[RawDataOutput],
            user_raw_data_outputs: List[RawDataOutput],
            search_run_context: Optional[SearchRunContext] = None,
            web_client: Optional[WebClient] = None
    ):
        """Constructor to create object."""
        self.search_run_context = SearchRunContext() if search_run_context is None \
            else search_run_context
        self.search_tweets_task = search_tweets_task
        self.tweet_raw_data_outputs = tweet_raw_data_outputs
        self.user_raw_data_outputs = user_raw_data_outputs
        self.web_client = web_client \
            if web_client is not None \
            else DefaultTwitterWebClientProvider.get_web_client()
        return

    def run(self) -> SearchTweetsResult:
        """Main search_runner method."""
        while not self._is_end_of_scrapping():
            self._execute_next_tweets_request()
        return SearchTweetsResult(self.search_run_context.all_download_tweets_count)

    def _is_end_of_scrapping(self) -> bool:
        ctx = self.search_run_context
        last_scrap_zero = ctx.last_tweets_download_count == 0
        is_cursor = ctx.cursor is not None
        return (last_scrap_zero and is_cursor) or (not last_scrap_zero and not is_cursor)

    def _execute_next_tweets_request(self):
        request_params = self._get_next_request_details()
        response = self.web_client.run_request(request_params)
        if response.is_success():
            tweets = parse_tweets(response.text)
            users = parse_users(response.text)
            cursor = get_scroll_cursor(json.loads(response.text)['timeline']['instructions'])
            self.search_run_context.add_downloaded_tweets_count(len(tweets))
            self.search_run_context.cursor = cursor
            self._process_new_results_to_output(tweets, users)
        else:
            raise ScrapBatchBadResponse(response)
        return

    def _get_next_request_details(self) -> RequestDetails:
        return TwitterApiRequests().get_search_tweet_request_details_new_api(
            self.search_run_context.all_download_tweets_count,
            self.search_run_context.cursor,
            self.search_tweets_task.tweets_limit,
            self.search_tweets_task.get_full_search_query()
        )

    def _process_new_results_to_output(self, tweets: List[TweetRaw], users: List[UserRaw]):
        for raw_data_output in self.tweet_raw_data_outputs:
            raw_data_output.export_raw_data(tweets)
        for raw_data_output in self.user_raw_data_outputs:
            raw_data_output.export_raw_data(users)
        return
