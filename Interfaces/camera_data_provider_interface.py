from abc import ABC, abstractmethod
from typing import List


class ICameraDataProvider(ABC):
    # @abstractmethod
    # def get_frame_at(self, time: datetime) -> 'frame':
    #     pass

    @abstractmethod
    def get_available_cameras(self) -> List[str]:
        pass

    @abstractmethod
    def initialize_capture(self, camera_index: int):
        pass

    @abstractmethod
    def is_ready(self) -> bool:
        pass

    @abstractmethod
    def end_capture(self):
        pass

    # TODO define return type
    @abstractmethod
    def get_next_frame(self):
        pass

    @abstractmethod
    def set_focus_callback(self, sender, data, user_data):
        # Note: user_data should be the tag of the associated UI element
        pass

    @abstractmethod
    def set_brightness_callback(self, sender, data, user_data):
        # Note: user_data should be the tag of the associated UI element
        pass

    @abstractmethod
    def reset_brightness_callback(self, sender, data, user_data):
        # Note: user_data should be the tag of the associated UI element
        pass

    @abstractmethod
    def set_autofocus_callback(self, sender, data, user_data):
        # Note: user_data should be the tag of the associated UI element
        pass
