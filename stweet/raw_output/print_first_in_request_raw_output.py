from typing import List

from .raw_data_output import RawDataOutput
from ..model.raw_data import RawData


class PrintFirstInRequestRawOutput(RawDataOutput):

    def export_raw_data(self, raw_data_list: List[RawData]):
        message = str(raw_data_list[0].to_json_line()) if len(
            raw_data_list) > 0 else 'PrintFirstInRequestTweetOutput -- no tweets to print'
        print(message)
        return
