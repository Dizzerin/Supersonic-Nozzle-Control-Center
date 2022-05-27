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
        """
        Method called to create/draw the window (place the UI elements etc.)
        :param viewport_width: width of the viewport (passed in from GUI_manager)
        :param viewport_height: height of the viewport (passed in from GUI_manager)
        :return: None
        """
        pass

    def show(self):
        dpg.configure_item(self.tag(), show=True)

    def hide(self):
        dpg.configure_item(self.tag(), show=False)

    def set_primary(self):
        dpg.set_primary_window(self.tag(), True)

    @abstractmethod
    def update(self):
        """
        Method called every frame
        :return: None
        """
        pass

