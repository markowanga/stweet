import json
from abc import ABC

from arrow import Arrow


class RawData(ABC):
    object_type: str
    download_datetime: Arrow
    raw_value: str

    def __init__(self, object_type: str, raw_value: str, download_datetime: Arrow):
        self.raw_value = raw_value
        self.object_type = object_type
        self.download_datetime = download_datetime

    def to_json_line(self) -> str:
        return json.dumps({
            'object_type': self.object_type,
            'download_datetime': self.download_datetime.isoformat(),
            'raw_value': json.loads(self.raw_value)
        })
