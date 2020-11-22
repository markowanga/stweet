"""Utils to parse data from web response."""

from abc import abstractmethod
from typing import List, Optional

from ..model.tweet import Tweet


class TweetParser:
    """Utils class to parse data from web response."""

    @abstractmethod
    def parse_tweets(self, response_text: str) -> List[Tweet]:
        """Method to extract tweets from web response."""

    @abstractmethod
    def parse_cursor(self, response_content: str) -> Optional[str]:
        """Method to extract next cursor to scrap request from web response."""
