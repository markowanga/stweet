"""Class with result of TweetSearchRunner task."""

from dataclasses import dataclass


@dataclass
class GetUsersResult:
    """Class with result of TweetSearchRunner task."""

    users_count: int
