from abc import ABC, abstractmethod
from Temp_Interfaces import custom_types
from datetime import datetime


class ICameraDataWriter(ABC):
    # TODO require input to be filehandle type
    def __init__(self, file):
        self.file = file

    @abstractmethod
    def write_camera_frame(self, frame_data: custom_types.DataRow, time: datetime) -> bool:
        pass
