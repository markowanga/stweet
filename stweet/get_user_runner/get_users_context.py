from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class GetUsersContext:
    scrapped_count: int = 0
    usernames_with_error: List[Tuple[str, Exception]] = field(default_factory=list)

    def add_one_scrapped_user(self):
        self.scrapped_count += 1

    def add_user_with_scrap_error(self, username: str, exception: Exception):
        self.usernames_with_error.append((username, exception))
