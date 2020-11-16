from dataclasses import dataclass
from typing import Optional


@dataclass
class RequestResponse:
    status_code: Optional[int]
    text: Optional[str]

    def is_token_expired(self) -> bool:
        return self.status_code == 429

    def is_success(self) -> bool:
        return self.status_code < 300
