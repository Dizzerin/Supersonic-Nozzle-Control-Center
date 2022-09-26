from abc import ABC, abstractmethod
from Custom_Types import custom_types
from datetime import datetime


class IADCDataWriter(ABC):
    # TODO require input to be filehandle type
    @abstractmethod
    def __init__(self, file):
        self.file = file

    @abstractmethod
    def set_recording_start_time(self):
        pass

    @abstractmethod
    def write_ADC_data(self, data: custom_types.SensorData, time: datetime) -> bool:
        pass
