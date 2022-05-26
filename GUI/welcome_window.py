import dearpygui.dearpygui as dpg
from GUI.window_interface import IWindow
from GUI import GUI_manager


class WelcomeWindow(IWindow):
    @staticmethod
    def tag() -> str:
        return "Welcome Window"

    def create(self):
        # Create first window (not hidden)
        with dpg.window(tag=self.tag(), show=True):
            dpg.add_text("This is the Welcome window")
            dpg.add_button(label="change window",
                           callback=lambda: GUI_manager.change_window(GUI_manager.LIVE_WINDOW))

