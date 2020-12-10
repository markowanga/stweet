"""Class with result of TweetSearchRunner task."""

from dataclasses import dataclass


@dataclass
class SearchTweetsResult:
    """Class with result of TweetSearchRunner task."""

    downloaded_count: int
