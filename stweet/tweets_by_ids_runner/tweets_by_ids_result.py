"""Class with result of TweetSearchRunner task."""

from dataclasses import dataclass
from typing import List


@dataclass
class TweetsByIdsResult:
    """Class with result of TweetSearchRunner task."""

    downloaded_count: int
    tweet_ids_not_scrapped: List[str]
