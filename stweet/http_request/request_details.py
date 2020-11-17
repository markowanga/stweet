from dataclasses import dataclass
from typing import Dict


@dataclass
class RequestDetails:
    url: str
    headers: Dict[str, str]
    params: Dict[str, str]
