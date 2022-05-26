import dearpygui.dearpygui as dpg
from abc import ABC, abstractmethod
"""
This uses a hybrid of functions and classes to try to manage and organize all window and window related functionality
"""

# Global (to this module) variables
LIVE_WINDOW = None
WELCOME_WINDOW = None
CURRENT_WINDOW = None


def init_GUI():
    global LIVE_WINDOW, WELCOME_WINDOW, CURRENT_WINDOW

    # Initialization for DPG
    dpg.create_context()
    dpg.create_viewport(title='Custom Title', width=600, height=200)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.maximize_viewport()

    # Instantiate window classes
    LIVE_WINDOW = LiveWindow()
    WELCOME_WINDOW = WelcomeWindow()

    # Create windows
    LIVE_WINDOW.create()
    WELCOME_WINDOW.create()

    # Set primary window
    dpg.set_primary_window(WELCOME_WINDOW.tag(), True)
    CURRENT_WINDOW = WELCOME_WINDOW


def run_GUI():
    # Start DPG
    # dpg.start_dearpygui()

    # Render Loop
    # (This replaces start_dearpygui() and runs every frame)
    while dpg.is_dearpygui_running():
        # Update
        # update_video(capture)
        # update_plots()

        # You can manually stop by using stop_dearpygui()
        dpg.render_dearpygui_frame()


def teardown_GUI():
    # Stop DPG
    dpg.destroy_context()


def change_window(to_window):
    """
    Used to change from one window to another (shows new window, sets it as primary, and hides the old)
    :param to_window: window object to set as the new primary and visible window
    :return: None
    """
    global CURRENT_WINDOW
    # Show new window
    dpg.configure_item(to_window.tag(), show=True)
    # Set it as the new main window
    dpg.set_primary_window(to_window.tag(), True)
    # Hide the old window
    dpg.configure_item(CURRENT_WINDOW.tag(), show=False)
    # Update current window global
    CURRENT_WINDOW = to_window


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
        global LIVE_WINDOW, WELCOME_WINDOW, CURRENT_WINDOW
        # Create first window (not hidden)
        with dpg.window(tag=self.tag(), show=True):
            dpg.add_text("This is the first window")
            dpg.add_button(label="change primary window",
                           callback=lambda: change_window(LIVE_WINDOW))


class LiveWindow(Window):
    @staticmethod
    def tag() -> str:
        return "Live Window"

    def create(self):
        global LIVE_WINDOW, WELCOME_WINDOW, CURRENT_WINDOW
        # Create second window (hidden)
        with dpg.window(tag=self.tag(), show=False):
            dpg.add_text("This is the second window")
            dpg.add_button(label="change primary window",
                           callback=lambda: change_window(WELCOME_WINDOW))


