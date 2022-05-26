import dearpygui.dearpygui as dpg
from abc import ABC, abstractmethod
"""
This uses classes to try to manage and organize all screen and window related functionality
Works!
But I don't like the layout and organization with the UI class...
Thinking of just letting all the functions in the UI class be standalone functions in this module
"""


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
        # Create first window (not hidden)
        with dpg.window(tag=self.tag(), show=True):
            dpg.add_text("This is the first window")
            dpg.add_button(label="change primary window",
                           callback=lambda: change_screen(UI.LiveScreen))


class LiveScreen(Screen):
    @staticmethod
    def tag() -> str:
        return "Live Screen"

    def create(self):
        # Create second window (hidden)
        with dpg.window(tag=self.tag(), show=False):
            dpg.add_text("This is the second window")
            dpg.add_button(label="change primary window",
                           callback=lambda: change_screen(UI.WelcomeScreen))


class UI:
    current_screen = None
    # Instantiate screen classes
    LiveScreen = LiveScreen()
    WelcomeScreen = WelcomeScreen()

    def __init__(self):
        # Initialization for DPG
        dpg.create_context()
        dpg.create_viewport(title='Custom Title', width=600, height=200)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.maximize_viewport()

        # Create screens
        self.LiveScreen.create()
        self.WelcomeScreen.create()

        # Set primary screen
        dpg.set_primary_window(self.WelcomeScreen.tag(), True)
        UI.current_screen = self.WelcomeScreen

        # Local vars

    def run(self):
        # Start DPG
        dpg.start_dearpygui()

    def teardown(self):
        # Stop DPG
        dpg.destroy_context()


def change_screen(to_screen):
    """
    Used to change from one screen to another (shows new screen, sets it as primary, and hides the old)
    :param to_screen: screen object to set as the new primary and visible screen
    :return: None
    """
    # Show new screen
    dpg.configure_item(to_screen.tag(), show=True)
    # Set it as the new main screen
    dpg.set_primary_window(to_screen.tag(), True)
    # Hide the old screen
    dpg.configure_item(UI.current_screen.tag(), show=False)
    # Update current screen variable
    UI.current_screen = to_screen
