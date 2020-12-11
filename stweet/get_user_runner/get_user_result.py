"""Class with result of TweetSearchRunner task."""

from dataclasses import dataclass

from ..model import User


@dataclass
class GetUserResult:
    """Class with result of TweetSearchRunner task."""

    user: User
