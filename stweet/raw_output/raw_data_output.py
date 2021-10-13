from abc import ABC, abstractmethod
from typing import List

from ..model.raw_data import RawData


class RawDataOutput(ABC):

    @abstractmethod
    def export_raw_data(self, raw_data_list: List[RawData]):
        pass
