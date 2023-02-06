from typing import List

from ..model.raw_data import RawData
from .raw_data_output import RawDataOutput


class CollectorRawOutput(RawDataOutput):
    _raw_data_list: List[RawData]

    def __init__(self):
        self._raw_data_list = []

    def export_raw_data(self, raw_data_list: List[RawData]):
        self._raw_data_list.extend(raw_data_list)
        return

    def get_raw_list(self) -> List[RawData]:
        return self._raw_data_list
