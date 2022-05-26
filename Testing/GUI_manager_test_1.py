import dearpygui.dearpygui as dpg
from abc import ABC, abstractmethod
"""
This uses classes to try to manage and organize all window and window related functionality
Works!
But I don't like the layout and organization with the UI class...
Thinking of just letting all the functions in the UI class be standalone functions in this module
"""


# Abstract base class which all windows implement
class Window(ABC):
    @staticmethod
    @abstractmethod
    def tag() -> str:
        pass

    @abstractmethod
    def create(self) -> 'Window':
        pass


class WelcomeWindow(Window):
    @staticmethod
    def tag() -> str:
        return "Welcome Window"

    def create(self):
        # Create first window (not hidden)
        with dpg.window(tag=self.tag(), show=True):
            dpg.add_text("This is the first window")
            dpg.add_button(label="change primary window",
                           callback=lambda: change_window(UI.LiveWindow))


class LiveWindow(Window):
    @staticmethod
    def tag() -> str:
        return "Live Window"

    def create(self):
        # Create second window (hidden)
        with dpg.window(tag=self.tag(), show=False):
            dpg.add_text("This is the second window")
            dpg.add_button(label="change primary window",
                           callback=lambda: change_window(UI.WelcomeWindow))


class UI:
    current_window = None
    # Instantiate window classes
    LiveWindow = LiveWindow()
    WelcomeWindow = WelcomeWindow()

    def __init__(self):
        # Initialization for DPG
        dpg.create_context()
        dpg.create_viewport(title='Custom Title', width=600, height=200)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.maximize_viewport()

        # Create windows
        self.LiveWindow.create()
        self.WelcomeWindow.create()

        # Set primary window
        dpg.set_primary_window(self.WelcomeWindow.tag(), True)
        UI.current_window = self.WelcomeWindow

        # Local vars

    def run(self):
        # Start DPG
        dpg.start_dearpygui()

    def teardown(self):
        # Stop DPG
        dpg.destroy_context()


def change_window(to_window):
    """
    Used to change from one window to another (shows new window, sets it as primary, and hides the old)
    :param to_window: window object to set as the new primary and visible window
    :return: None
    """
    # Show new window
    dpg.configure_item(to_window.tag(), show=True)
    # Set it as the new main window
    dpg.set_primary_window(to_window.tag(), True)
    # Hide the old window
    dpg.configure_item(UI.current_window.tag(), show=False)
    # Update current window variable
    UI.current_window = to_window
