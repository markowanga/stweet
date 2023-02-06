from typing import List

from ..model.raw_data import RawData
from .raw_data_output import RawDataOutput


class PrintEveryNRawOutput(RawDataOutput):
    each_n: int
    _counter: int = 0

    def __init__(self, each_n: int):
        self.each_n = each_n

    def export_raw_data(self, raw_data_list: List[RawData]):
        for it in raw_data_list:
            self._counter += 1
            if self._counter % self.each_n == 0:
                print(self._counter, it.to_json_line())
        return
