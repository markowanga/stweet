"""Class with result of TweetSearchRunner task."""

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class GetUsersResult:
    """Class with result of TweetSearchRunner task."""

    users_count: int
    usernames_with_error: List[Tuple[str, Exception]]
