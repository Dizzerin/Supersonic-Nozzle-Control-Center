from abc import ABC, abstractmethod
from dataclasses import dataclass
import datetime


class IVideoReader(ABC):

    @abstractmethod
    def get_frame_at(self, time: datetime) -> 'frame':
        pass

    @abstractmethod
    def get_next_frame(self) -> 'frame':
        pass


class IVideoWriter(ABC):

    @abstractmethod
    # Todo pass file handle?  return bool or just raise exception?
    def write_frame(self, frame: 'frame', time: datetime, file: filehandle) -> bool:
        pass


@dataclass
class DataRow:
    """
    Structure defining the values contained in a data row
    Each row has a timestamp associated with it, a temperature, and a number of pressure readings
    """
    time: datetime
    temp: float
    p1: float
    p2: float
    p3: float
    p4: float
    p5: float
    p6: float
    p7: float
    p8: float
    p9: float


class IDataReader(ABC):

    @abstractmethod
    def get_data_row_at(self, time: datetime) -> DataRow:
        pass

    @abstractmethod
    def get_next_data_row(self) -> DataRow:
        pass


class IDataWriter(ABC):

    @abstractmethod
    # Todo pass file handle?  return bool or just raise exception?
    def write_frame(self, data: DataRow, time: datetime, file: filehandle) -> bool:
        pass
