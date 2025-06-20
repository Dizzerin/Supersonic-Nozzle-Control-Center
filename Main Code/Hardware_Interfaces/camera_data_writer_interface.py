from abc import ABC, abstractmethod
from Custom_Types import custom_types
from datetime import datetime


class ICameraDataWriter(ABC):
    # TODO (skip) require input to be filehandle type
    def __init__(self, file):
        self.file = file

    @abstractmethod
    def write_camera_frame(self, frame_data: custom_types.SensorData, time: datetime) -> bool:
        pass
