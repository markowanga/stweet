"""Class with request details."""

from dataclasses import dataclass
from typing import Dict


@dataclass
class RequestDetails:
    """Class with request details. Specify all http request details."""

    url: str
    headers: Dict[str, str]
    params: Dict[str, str]
