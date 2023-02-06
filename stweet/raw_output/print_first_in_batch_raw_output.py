from typing import List

from ..model.raw_data import RawData
from .raw_data_output import RawDataOutput


class PrintFirstInBatchRawOutput(RawDataOutput):

    def export_raw_data(self, raw_data_list: List[RawData]):
        message = str(raw_data_list[0].to_json_line()) if len(
            raw_data_list) > 0 else 'PrintFirstInRequestTweetOutput -- no tweets to print'
        print(message)
        return
