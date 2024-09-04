from abc import ABC, abstractmethod
from Custom_Types.custom_types import SensorData, SensorDataTimed
from datetime import datetime


class IADCDataWriter(ABC):
    # TODO (optional) require input to be filehandle type
    @abstractmethod
    def __init__(self, file):
        self.file = file

    @abstractmethod
    def write_ADC_data(self, sensor_data_timed: SensorDataTimed) -> bool:
        pass

    @abstractmethod
    def close_file(self):
        pass

