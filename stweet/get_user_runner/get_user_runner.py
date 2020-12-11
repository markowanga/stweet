"""Runner for get tweets by ids."""
from dataclasses import dataclass
from typing import Optional

from .get_user_context import GetUserContext
from .get_user_request_details_builder import get_user_details_request_details
from .get_user_result import GetUserResult
from .get_user_task import GetUserTask
from .user_parser import parse_user
from ..auth import AuthTokenProviderFactory, SimpleAuthTokenProviderFactory
from ..http_request import WebClient
from ..http_request.web_client_requests import WebClientRequests
from ..search_runner.parse import BaseTweetParser
from ..search_runner.parse import TweetParser


@dataclass
class _TweetByIdBaseInfo:
    id: str
    username: str
    tweet_content: str


class GetUserRunner:
    """Runner class to process task to search tweets."""

    get_user_context: GetUserContext
    get_user_task: GetUserTask
    web_client: WebClient
    tweet_parser: TweetParser
    auth_token_provider_factory: AuthTokenProviderFactory

    def __init__(
            self,
            get_user_task: GetUserTask,
            get_user_context: Optional[GetUserContext] = None,
            web_client: WebClient = WebClientRequests(),
            tweet_parser: TweetParser = BaseTweetParser(),
            auth_token_provider_factory: AuthTokenProviderFactory = SimpleAuthTokenProviderFactory()
    ):
        """Constructor to create object."""
        self.get_user_context = GetUserContext() if get_user_context is None else get_user_context
        self.get_user_task = get_user_task
        self.web_client = web_client
        self.tweet_parser = tweet_parser
        self.auth_token_provider_factory = auth_token_provider_factory
        return

    def run(self) -> GetUserResult:
        """Main search_runner method."""
        self._prepare_token()
        request_details = get_user_details_request_details(self.get_user_task.username, self.get_user_context)
        user_request_response = self.web_client.run_request(request_details)
        return GetUserResult(parse_user(user_request_response.text))

    def _refresh_token(self):
        token_provider = self.auth_token_provider_factory.create(self.web_client)
        self.get_user_context.guest_auth_token = token_provider.get_new_token()
        return

    def _prepare_token(self):
        if self.get_user_context.guest_auth_token is None:
            self._refresh_token()
        return
