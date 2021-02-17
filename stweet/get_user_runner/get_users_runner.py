"""Runner for get tweets by ids."""
from dataclasses import dataclass
from typing import Optional, List

from stweet.http_request.requests.requests_web_client import RequestsWebClient
from .get_user_request_details_builder import get_user_details_request_details
from .get_users_context import GetUsersContext
from .get_users_result import GetUsersResult
from .get_users_task import GetUsersTask
from .user_parser import parse_user
from ..auth import AuthTokenProviderFactory, SimpleAuthTokenProviderFactory
from ..http_request import WebClient
from ..http_request.interceptor.params_response_log_web_client_interceptor import ParamsResponseLogWebClientInterceptor
from ..model import User
from ..user_output import UserOutput


@dataclass
class _TweetByIdBaseInfo:
    id: str
    username: str
    tweet_content: str


class GetUsersRunner:
    """Runner class to process task to search tweets."""

    get_user_context: GetUsersContext
    get_user_task: GetUsersTask
    user_outputs: List[UserOutput]
    web_client: WebClient
    auth_token_provider_factory: AuthTokenProviderFactory

    def __init__(
            self,
            get_user_task: GetUsersTask,
            user_outputs: List[UserOutput],
            get_user_context: Optional[GetUsersContext] = None,
            web_client: WebClient = RequestsWebClient(interceptors=[ParamsResponseLogWebClientInterceptor()]),
            auth_token_provider_factory: AuthTokenProviderFactory = SimpleAuthTokenProviderFactory()
    ):
        """Constructor to create object."""
        self.get_user_context = GetUsersContext() if get_user_context is None else get_user_context
        self.get_user_task = get_user_task
        self.user_outputs = user_outputs
        self.web_client = web_client
        self.auth_token_provider_factory = auth_token_provider_factory
        return

    def run(self) -> GetUsersResult:
        """Main search_runner method."""
        for username in self.get_user_task.usernames:
            self._try_get_user(username)
        return GetUsersResult(self.get_user_context.scrapped_count, self.get_user_context.usernames_with_error)

    def _try_get_user(self, username: str):
        try:
            request_details = get_user_details_request_details(username, self.get_user_context)
            user_request_response = self.web_client.run_request(request_details)
            full_user = parse_user(user_request_response.text)
            self.get_user_context.add_one_scrapped_user()
            self._process_user_to_output(full_user)
        except Exception as exception:
            self.get_user_context.add_user_with_scrap_error(username, exception)

    def _process_user_to_output(self, user: User):
        for user_output in self.user_outputs:
            user_output.export_users([user])
