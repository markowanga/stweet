"""Class with response details."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class RequestResponse:
    """Class with response details. Independent of web library implementation."""

    status_code: Optional[int]
    text: Optional[str]

    def is_token_expired(self) -> bool:
        """Method to check that is token_expired response status."""
        return self.status_code == 429

    def is_success(self) -> bool:
        """Method to check that response have success status."""
        return self.status_code is not None and self.status_code < 300
