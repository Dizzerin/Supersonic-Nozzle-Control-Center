import dearpygui.dearpygui as dpg
from GUI.window_interface import IWindow
from GUI import GUI_manager


class LiveWindow(IWindow):
    @staticmethod
    def tag() -> str:
        return "Live Window"

    def create(self, viewport_width: int, viewport_height: int):
        # Local vars


        # Create textures which will later be added to the window



        # Build the window
        with dpg.window(tag=self.tag(), show=False):
            dpg.add_text("This is the Live Window")
            dpg.add_button(label="change window",
                           callback=lambda: GUI_manager.change_window(GUI_manager.WELCOME_WINDOW))


