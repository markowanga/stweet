"""Class with result of TweetSearchRunner task."""

from dataclasses import dataclass


@dataclass
class TweetsByIdsResult:
    """Class with result of TweetSearchRunner task."""

    downloaded_count: int
