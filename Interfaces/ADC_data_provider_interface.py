from abc import ABC, abstractmethod
from Temp_Interfaces import custom_types


class IADCDataProvider(ABC):

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def is_initialized(self) -> bool:
        # Indicates the device was found, initialized, and communication has been established
        pass

    @abstractmethod
    def is_calibrated(self) -> bool:
        # Indicates the device has been calibrated and proper readings can be obtained
        pass

    @abstractmethod
    # TODO implement the use of this
    def set_acquisition_start_time(self):
        pass

    @abstractmethod
    def calibrate(self, atmospheric_psi: float):
        pass

    @abstractmethod
    def get_next_data_row(self) -> custom_types.SensorData:
        pass
