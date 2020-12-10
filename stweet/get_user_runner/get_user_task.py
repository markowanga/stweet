"""Domain GetUserTask class."""
from dataclasses import dataclass


@dataclass(frozen=True)
class GetUserTask:
    """Domain GetUserTask class."""

    username: str

    def __init__(
            self,
            username: str
    ):
        """Class constructor."""
        object.__setattr__(self, 'username', username)
        return
