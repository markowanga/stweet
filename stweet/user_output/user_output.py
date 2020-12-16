"""Generic class to process user output."""

from abc import ABC, abstractmethod
from typing import List

from ..model import User


class UserOutput(ABC):
    """Generic class to process user output."""

    @abstractmethod
    def export_users(self, tweets: List[User]):
        """Method to process all users from request batch."""
