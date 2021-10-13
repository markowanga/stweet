from dataclasses import dataclass


@dataclass
class Cursor:
    type: str
    value: str
