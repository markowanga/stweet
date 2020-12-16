"""UserOutput which saves user data in memory, after request can return all saved users."""
from typing import List

from .user_output import UserOutput
from ..model import User


class CollectorUserOutput(UserOutput):
    """UserOutput which print first user from request batch."""

    _users: List[User]

    def __init__(self):
        """Constructor of class, initialize users as empty list."""
        self._users = []

    def export_users(self, users: List[User]):
        """Method print first user in console, when users list is empty there message will be printed."""
        self._users.extend(users)
        return

    def get_scrapped_users(self) -> List[User]:
        """Method returns all collected users."""
        return self._users
