from abc import ABC, abstractmethod
from Temp_Interfaces import custom_types


class IADCDataProvider(ABC):

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def is_ready(self) -> bool:
        pass

    @abstractmethod
    def calibrate(self):
        pass

    @abstractmethod
    def get_next_data_row(self) -> custom_types.DataRow:
        pass
