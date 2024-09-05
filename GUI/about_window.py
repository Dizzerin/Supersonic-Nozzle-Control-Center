import dearpygui.dearpygui as dpg
from Software_Interfaces.window_interface import IWindow
from GUI import GUI_manager


class AboutWindow(IWindow):
    def __init__(self):
        # Call super class's init
        super(AboutWindow, self).__init__()

        # Local vars
        self.is_created = False

    def is_created(self) -> bool:
        return self.is_created

    def tag(self) -> str:
        return "About Window"

    def include_title_bar(self) -> bool:
        return False

    def update(self):
        pass

    def create(self, viewport_width: int, viewport_height: int):
        # Don't show title bar
        dpg.set_viewport_decorated(self.include_title_bar())
        # dpg.maximize_viewport()

        # Local vars
        # Note: These are only used for the button on this screen
        # Todo (optional) maybe implement some of this as a style and make the text larger and apply the style to these buttons instead
        button_y_start = viewport_height / 2 + 60
        button_width = 150
        button_height = 35
        button_y_spacing = 60  # Number of vertical pixels between top of one button to top of next only for Welcome Window buttons

        # Title positioning
        title_y_start = viewport_height / 2 - 70

        # Build main welcome window
        with dpg.window(tag=self.tag(), show=True):
            # Add background image (this depends on this already being created and in the texture registry)
            dpg.add_image("background_image", pos=[0, 0])

            # Add title/subtitle text
            dpg.add_text("ABOUT", pos=[int(viewport_width / 2 - 30), title_y_start])
            dpg.add_text("Supersonic Nozzle Control Center v0.1.0", pos=[int(viewport_width / 2 - 150), title_y_start + 40])

            # Add github link
            dpg.add_text("To access project source code, visit:\n"
                         "https://github.com/Dizzerin/Supersonic-Nozzle-Control-Center",
                         pos=[int(viewport_width / 2 - 150), title_y_start + 70])

            # Add buttons
            dpg.add_button(label="Take me back!", width=button_width, height=button_height,
                       pos=[int(viewport_width / 2 - button_width / 2), button_y_start + 0 * button_y_spacing],
                       callback=lambda: GUI_manager.change_window(GUI_manager.WELCOME_WINDOW))

        # Indicate that this window has been created
        self.is_created = True
