from dataclasses import dataclass
from typing import List, Optional

from ..http_request import WebClient
from ..model.user_raw import UserRaw
from ..raw_output.raw_data_output import RawDataOutput
from ..twitter_api.default_twitter_web_client_provider import \
    DefaultTwitterWebClientProvider
from ..twitter_api.twitter_api_requests import TwitterApiRequests
from .get_users_context import GetUsersContext
from .get_users_result import GetUsersResult
from .get_users_task import GetUsersTask
from .user_parser import parse_user


@dataclass
class _TweetByIdBaseInfo:
    id: str
    username: str
    tweet_content: str


class GetUsersRunner:

    get_user_context: GetUsersContext
    get_user_task: GetUsersTask
    raw_data_outputs: List[RawDataOutput]
    web_client: WebClient

    def __init__(
            self,
            get_user_task: GetUsersTask,
            raw_data_outputs: List[RawDataOutput],
            get_user_context: Optional[GetUsersContext] = None,
            web_client: Optional[WebClient] = None
    ):
        self.get_user_context = GetUsersContext() if get_user_context is None else get_user_context
        self.get_user_task = get_user_task
        self.raw_data_outputs = raw_data_outputs
        self.web_client = web_client if web_client is not None \
            else DefaultTwitterWebClientProvider.get_web_client()
        return

    def run(self) -> GetUsersResult:
        for username in self.get_user_task.usernames:
            self._try_get_user(username)
        return GetUsersResult(self.get_user_context.scrapped_count,
                              self.get_user_context.usernames_with_error)

    def _try_get_user(self, username: str):
        try:
            request_details = TwitterApiRequests().get_user_details_request_details(username)
            user_request_response = self.web_client.run_request(request_details)
            full_user = parse_user(user_request_response.text)
            self.get_user_context.add_one_scrapped_user()
            self._process_user_to_output(full_user)
        except Exception as exception:
            self.get_user_context.add_user_with_scrap_error(username, exception)

    def _process_user_to_output(self, user_raw: UserRaw):
        for user_output in self.raw_data_outputs:
            user_output.export_raw_data([user_raw])
