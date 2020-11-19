"""Class with result of TweetSearchRunner task."""

from dataclasses import dataclass
from typing import List, Optional

from ..model import Tweet


@dataclass
class SearchTweetsResult:
    """Class with result of TweetSearchRunner task.

    Tweets field is filled when task config is set to return tweets in memory.
    """

    downloaded_count: int
    tweets: Optional[List[Tweet]]
