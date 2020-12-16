"""Domain GetUsersTask class."""
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class GetUsersTask:
    """Domain GetUsersTask class."""

    usernames: List[str]

    def __init__(
            self,
            usernames: List[str]
    ):
        """Class constructor."""
        object.__setattr__(self, 'usernames', usernames)
        return
