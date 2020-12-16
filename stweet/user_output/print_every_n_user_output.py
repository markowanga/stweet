"""UserOutput which print each n-th tweet."""

from typing import List

from .user_output import UserOutput
from ..model import User


class PrintEveryNUserOutput(UserOutput):
    """UserOutput which print each n-th user."""

    each_n: int
    _counter: int = 0

    def __init__(self, each_n: int):
        """Create instance of PrintEveryNUserOutput."""
        self.each_n = each_n

    def export_users(self, users: List[User]):
        """Method print first each n user in console with all scrapped count."""
        for it in users:
            self._counter += 1
            if self._counter % self.each_n == 0:
                print(self._counter, it)
        return
