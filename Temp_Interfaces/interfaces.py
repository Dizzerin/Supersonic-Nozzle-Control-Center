from abc import ABC, abstractmethod
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
