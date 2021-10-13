from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class GetUsersTask:
    usernames: List[str]

    def __init__(
            self,
            usernames: List[str]
    ):
        object.__setattr__(self, 'usernames', usernames)
        return
