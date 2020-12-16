"""UserOutput which print all users from request batch."""

from typing import List

from .user_output import UserOutput
from ..model import User


class PrintUserOutput(UserOutput):
    """UserOutput which print all users from request batch."""

    def export_users(self, users: List[User]):
        """Print all users from list."""
        for it in users:
            print(it)
        return
