"""Class with result of TweetSearchRunner task."""

from dataclasses import dataclass
from typing import List


@dataclass
class TweetsByIdResult:
    """Class with result of TweetSearchRunner task."""

    downloaded_count: int
