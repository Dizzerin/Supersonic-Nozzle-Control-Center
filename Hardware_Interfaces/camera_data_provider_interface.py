from abc import ABC, abstractmethod
from typing import List

class CameraError(Exception):
    """Custom exception for camera-related errors."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ICameraDataProvider(ABC):
    def __init__(self, width, height):
        pass

    # @abstractmethod
    # def get_frame_at(self, time: datetime) -> 'frame':
    #     pass

    @abstractmethod
    def get_width(self) -> int:
        pass

    @abstractmethod
    def get_height(self) -> int:
        pass

    @abstractmethod
    def get_available_cameras(self) -> List[int]:
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
        pass

    @abstractmethod
    def set_brightness_callback(self, sender, data, user_data):
        pass

    @abstractmethod
    def reset_brightness_callback(self, sender, data, user_data):
        pass

    @abstractmethod
    def set_autofocus_callback(self, sender, data, user_data):
        pass

    @abstractmethod
    def reset_all_brightness_and_focus_settings(self, focus_slider_tag, AF_checkbox_tag, brightness_slider_tag):
        pass
