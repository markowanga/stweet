from typing import List

from ..model.raw_data import RawData
from .raw_data_output import RawDataOutput


class JsonLineFileRawOutput(RawDataOutput):
    file_name: str

    def __init__(self, file_name: str):
        self.file_name = file_name

    def export_raw_data(self, raw_data_list: List[RawData]):
        with open(self.file_name, 'a') as file:
            for raw in raw_data_list:
                file.write(f'{raw.to_json_line()}\n')
        return
