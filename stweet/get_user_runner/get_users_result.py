"""Class with result of GetUsersRunner task."""

from dataclasses import dataclass


@dataclass
class GetUsersResult:
    """Class with result of GetUsersRunner task."""

    users_count: int
