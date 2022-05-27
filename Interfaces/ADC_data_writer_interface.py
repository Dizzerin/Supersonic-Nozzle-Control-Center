from abc import ABC, abstractmethod
from Temp_Interfaces import custom_types
from datetime import datetime


class IADCDataWriter(ABC):
    # TODO require input to be filehandle type
    def __init__(self, file):
        self.file = file

    @abstractmethod
    def write_ADC_data(self, data: custom_types.DataRow, time: datetime) -> bool:
        pass
