"""Runner for get tweets by ids."""
import json
from typing import List, Optional

from ..exceptions import ScrapBatchBadResponse
from ..http_request import RequestDetails, RequestResponse, WebClient
from ..model import UserTweetRaw
from ..model.cursor import Cursor
from ..raw_output.raw_data_output import RawDataOutput
from ..twitter_api.default_twitter_web_client_provider import \
    DefaultTwitterWebClientProvider
from ..twitter_api.twitter_api_requests import TwitterApiRequests
from .tweet_raw_parser import get_all_tweets_from_json
from .tweets_by_id_context import TweetsByIdContext
from .tweets_by_id_result import TweetsByIdResult
from .tweets_by_id_task import TweetsByIdTask

_NOT_FOUND_MESSAGE = '_Missing: No status found with that ID.'


class TweetsByIdRunner:
    tweets_by_id_context: TweetsByIdContext
    tweets_by_ids_task: TweetsByIdTask
    raw_data_outputs: List[RawDataOutput]
    web_client: WebClient

    def __init__(
            self,
            tweets_by_id_task: TweetsByIdTask,
            raw_data_outputs: List[RawDataOutput],
            tweets_by_ids_context: Optional[TweetsByIdContext] = None,
            web_client: Optional[WebClient] = None,
    ):
        self.tweets_by_id_context = TweetsByIdContext() if tweets_by_ids_context is None \
            else tweets_by_ids_context
        self.tweets_by_ids_task = tweets_by_id_task
        self.raw_data_outputs = raw_data_outputs
        self.web_client = web_client if web_client is not None \
            else DefaultTwitterWebClientProvider.get_web_client()
        return

    def run(self) -> TweetsByIdResult:
        """Main search_runner method."""
        while not self._is_end_of_scrapping():
            self._execute_next_tweets_request()
        return TweetsByIdResult(self.tweets_by_id_context.all_download_tweets_count)

    def _is_end_of_scrapping(self) -> bool:
        ctx = self.tweets_by_id_context
        is_cursor = ctx.cursor is not None
        was_any_call = ctx.requests_count > 0
        return was_any_call and not is_cursor

    @staticmethod
    def response_with_not_found(request_response: RequestResponse) -> bool:
        parsed = json.loads(request_response.text)
        if 'errors' not in parsed:
            return False
        errors = parsed['errors']
        filtered_errors = [it for it in errors if _NOT_FOUND_MESSAGE == it['message']]
        return len(filtered_errors) > 0

    def _execute_next_tweets_request(self):
        request_params = self._get_next_request_details()
        response = self.web_client.run_request(request_params)
        if response.is_success():
            if self.response_with_not_found(response):
                self.tweets_by_id_context.add_downloaded_tweets_count_in_request(0)
                self.tweets_by_id_context.cursor = None
            else:
                parsed_list = get_all_tweets_from_json(response.text)
                cursors = [it for it in parsed_list if isinstance(it, Cursor)]
                cursor = cursors[0] if len(cursors) > 0 else None
                user_tweet_raw = [it for it in parsed_list if isinstance(it, UserTweetRaw)]
                self.tweets_by_id_context.add_downloaded_tweets_count_in_request(len(user_tweet_raw))
                self.tweets_by_id_context.cursor = cursor
                self._process_new_tweets_to_output(user_tweet_raw)
        else:
            raise ScrapBatchBadResponse(response)
        return

    def _process_new_tweets_to_output(self, raw_data_list: List[UserTweetRaw]):
        for raw_output in self.raw_data_outputs:
            raw_output.export_raw_data(raw_data_list)
        return

    def _get_next_request_details(self) -> RequestDetails:
        return TwitterApiRequests().get_tweet_request_by_id(
            self.tweets_by_ids_task.tweet_id,
            self.tweets_by_id_context.cursor
        )
