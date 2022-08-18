from abc import ABC, abstractmethod
from Temp_Interfaces.custom_types import PressureSensorConfigData, TemperatureSensorSettingsData
from typing import List


class IConfigFileHandler(ABC):
    @abstractmethod
    def __init__(self, config_filepath):
        self.config_file = config_filepath

    @abstractmethod
    def get_default_save_location(self) -> str:
        pass

    @abstractmethod
    def get_default_camera_index(self) -> int:
        pass

    @abstractmethod
    def get_camera_width(self) -> int:
        pass

    @abstractmethod
    def get_camera_height(self) -> int:
        pass

    @abstractmethod
    def get_pressure_sensors(self) -> List[PressureSensorConfigData]:
        pass

    @abstractmethod
    def get_temperature_sensors(self) -> List[TemperatureSensorSettingsData]:
        pass

    @abstractmethod
    def set_default_save_location(self, filepath: str):
        pass

    @abstractmethod
    def set_default_camera_index(self, index: int):
        pass

    @abstractmethod
    def set_camera_width(self, width: int):
        pass

    @abstractmethod
    def set_camera_height(self, height: int):
        pass

    @abstractmethod
    def set_pressure_sensor(self, pressure_sensor: PressureSensorConfigData):
        pass

    @abstractmethod
    def set_temperature_sensor(self, temperature_sensor: TemperatureSensorSettingsData):
        pass

    @abstractmethod
    def write_config_file(self):
        pass

