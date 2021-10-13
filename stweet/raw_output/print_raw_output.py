from typing import List

from .raw_data_output import RawDataOutput
from ..model.raw_data import RawData


class PrintRawOutput(RawDataOutput):

    def export_raw_data(self, raw_data_list: List[RawData]):
        for it in raw_data_list:
            print(it.to_json_line())
        return
