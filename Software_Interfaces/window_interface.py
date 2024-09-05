from abc import ABC, abstractmethod
import dearpygui.dearpygui as dpg
# from typing import Type


# Abstract base class which all windows implement
class IWindow(ABC):
    @abstractmethod
    def is_created(self) -> bool:
        pass

    @abstractmethod
    def tag(self) -> str:
        # Way of requiring member variable on child classes essentially
        # (didn't use @property decorator because I don't want to define getters and setters)
        pass

    @abstractmethod
    def include_title_bar(self) -> bool:
        # Way of requiring member variable on child classes essentially
        # (didn't use @property decorator because I don't want to define getters and setters)
        pass

    @abstractmethod
    def create(self, viewport_width: int, viewport_height: int):
        # TODO (optional) maybe make this all take place in each class's init instead
        #   and avoid globals
        """
        Method called to create/draw the window (place the UI elements etc.)
        :param viewport_width: width of the viewport (passed in from GUI_manager)
        :param viewport_height: height of the viewport (passed in from GUI_manager)
        :return: None
        """
        pass

    def show(self):
        # Show/hide title bar according to window's setting
        # dpg.set_viewport_decorated(self.include_title_bar())
        # dpg.maximize_viewport()
        # Show the window
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
