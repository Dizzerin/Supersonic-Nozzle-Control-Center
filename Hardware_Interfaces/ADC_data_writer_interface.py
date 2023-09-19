from abc import ABC, abstractmethod
from Custom_Types.custom_types import SensorData
from datetime import datetime


class IADCDataWriter(ABC):
    # TODO require input to be filehandle type
    @abstractmethod
    def __init__(self, file):
        self.file = file

    @abstractmethod
    def set_logging_start_time(self):
        pass

    @abstractmethod
    def write_ADC_data(self, sensor_data: SensorData, time: datetime) -> bool:
        pass

    @abstractmethod
    def save_file(self):
        pass

