from abc import ABC, abstractmethod
from Custom_Types.custom_types import PressureSensorConfigData, TemperatureSensorConfigData, ConfigSettings
from typing import List


class IConfigHandler(ABC):
    @abstractmethod
    def get_default_save_directory(self) -> str:
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
    def get_temperature_sensors(self) -> List[TemperatureSensorConfigData]:
        pass

    @abstractmethod
    def set_default_save_directory(self, filepath: str):
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
    def set_temperature_sensor(self, temperature_sensor: TemperatureSensorConfigData):
        pass

    @abstractmethod
    def set_config_settings(self, config_settings: ConfigSettings):
        pass

    @abstractmethod
    def write_config_file(self):
        pass

