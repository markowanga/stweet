from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class GetUsersResult:
    users_count: int
    usernames_with_error: List[Tuple[str, Exception]]
