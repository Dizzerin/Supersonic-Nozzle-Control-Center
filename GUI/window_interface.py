from abc import ABC, abstractmethod
import dearpygui.dearpygui as dpg
# from typing import Type


# Abstract base class which all windows implement
class IWindow(ABC):
    @staticmethod
    @abstractmethod
    def tag() -> str:
        pass

    @abstractmethod
    def create(self, viewport_width: int, viewport_height: int):
        pass

    def show(self):
        dpg.configure_item(self.tag(), show=True)

    def hide(self):
        dpg.configure_item(self.tag(), show=False)

    def set_primary(self):
        dpg.set_primary_window(self.tag(), True)

    # @abstractmethod
    # def update(self) -> Optional["IWindow"]:
    #     pass

