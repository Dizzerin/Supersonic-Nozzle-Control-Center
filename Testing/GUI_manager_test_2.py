import dearpygui.dearpygui as dpg
from abc import ABC, abstractmethod
"""
This uses a hybrid of functions and classes to try to manage and organize all screen and window related functionality
"""

# Global (to this module) variables
LIVE_SCREEN = None
WELCOME_SCREEN = None
CURRENT_SCREEN = None


def init_GUI():
    global LIVE_SCREEN, WELCOME_SCREEN, CURRENT_SCREEN

    # Initialization for DPG
    dpg.create_context()
    dpg.create_viewport(title='Custom Title', width=600, height=200)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.maximize_viewport()

    # Instantiate screen classes
    LIVE_SCREEN = LiveScreen()
    WELCOME_SCREEN = WelcomeScreen()

    # Create screens
    LIVE_SCREEN.create()
    WELCOME_SCREEN.create()

    # Set primary screen
    dpg.set_primary_window(WELCOME_SCREEN.tag(), True)
    CURRENT_SCREEN = WELCOME_SCREEN


def run_GUI():
    # Start DPG
    dpg.start_dearpygui()


def teardown_GUI():
    # Stop DPG
    dpg.destroy_context()


def change_screen(to_screen):
    """
    Used to change from one screen to another (shows new screen, sets it as primary, and hides the old)
    :param to_screen: screen object to set as the new primary and visible screen
    :return: None
    """
    global CURRENT_SCREEN
    # Show new screen
    dpg.configure_item(to_screen.tag(), show=True)
    # Set it as the new main screen
    dpg.set_primary_window(to_screen.tag(), True)
    # Hide the old screen
    dpg.configure_item(CURRENT_SCREEN.tag(), show=False)
    # Update current screen global
    CURRENT_SCREEN = to_screen


# Abstract base class which all screens implement
class Screen(ABC):
    @staticmethod
    @abstractmethod
    def tag() -> str:
        pass

    @abstractmethod
    def create(self) -> 'Screen':
        pass


class WelcomeScreen(Screen):
    @staticmethod
    def tag() -> str:
        return "Welcome Screen"

    def create(self):
        global LIVE_SCREEN, WELCOME_SCREEN, CURRENT_SCREEN
        # Create first window (not hidden)
        with dpg.window(tag=self.tag(), show=True):
            dpg.add_text("This is the first window")
            dpg.add_button(label="change primary window",
                           callback=lambda: change_screen(LIVE_SCREEN))


class LiveScreen(Screen):
    @staticmethod
    def tag() -> str:
        return "Live Screen"

    def create(self):
        global LIVE_SCREEN, WELCOME_SCREEN, CURRENT_SCREEN
        # Create second window (hidden)
        with dpg.window(tag=self.tag(), show=False):
            dpg.add_text("This is the second window")
            dpg.add_button(label="change primary window",
                           callback=lambda: change_screen(WELCOME_SCREEN))


