"""Class with request details."""

from dataclasses import dataclass
from typing import Dict

from ..http_request.http_method import HttpMethod


@dataclass
class RequestDetails:
    """Class with request details. Specify all http request details."""

    http_method: HttpMethod
    url: str
    headers: Dict[str, str]
    params: Dict[str, str]
    timeout: int
