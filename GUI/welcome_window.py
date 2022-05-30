import dearpygui.dearpygui as dpg
from Interfaces.window_interface import IWindow
from GUI import GUI_manager


class WelcomeWindow(IWindow):
    def __init__(self):
        # Call super class's init
        super(WelcomeWindow, self).__init__()

        # Local vars
        self.is_created = False

        # TODO create rounded transparent button style and apply to buttons on this screen

    def is_created(self) -> bool:
        return self.is_created

    def tag(self) -> str:
        return "Welcome Window"

    def include_title_bar(self) -> bool:
        return False

    def update(self):
        pass

    def create(self, viewport_width: int, viewport_height: int):
        # Local vars
        # Note: These are only used for the button on this screen
        # Todo maybe implement some of this as a style and make the text larger and apply the style to these buttons instead
        button_y_start = viewport_height / 2 + 80
        button_width = 150
        button_height = 35
        button_y_spacing = 60  # Number of vertical pixels between top of one button to top of next only for Welcome Window buttons

        # Title positioning
        title_y_start = 100

        # Create textures/images (which will later be added to the window)
        width1, height1, channels1, data1 = dpg.load_image(r"Image_Resources/Logo2.png")
        width2, height2, channels2, data2 = dpg.load_image(r"Image_Resources/WelcomeScreenBackground.png")
        with dpg.texture_registry():
            dpg.add_static_texture(width=width1, height=height1, default_value=data1, tag="title_image")
            dpg.add_static_texture(width=width2, height=height2, default_value=data2, tag="background_image")

        # Build the window
        with dpg.window(tag=self.tag(), show=True):

            # Add background image
            dpg.add_image("background_image", pos=[0, 0])

            # Add title/logo image
            # dpg.add_image("title_image", pos=[550, title_y_start])
            # TODO figure out why the below doesn't work
            # helper_functions.center_x("title_image")

            # Add title/subtitle text
            # dpg.add_text("WELCOME", pos=[int(viewport_width / 2 - 50), title_y_start])
            # dpg.add_text("Supersonic Nozzle Control Center 0.1.0", pos=[int(viewport_width / 2 - 150), title_y_start + 30])

            # Add buttons
            dpg.add_button(label="Live Session", width=button_width, height=button_height,
                           pos=[int(viewport_width / 2 - button_width / 2), button_y_start + 0 * button_y_spacing],
                           callback=lambda: GUI_manager.change_window(GUI_manager.INITIALIZATION_WINDOW))
            dpg.add_button(label="Settings", width=button_width, height=button_height,
                           pos=[int(viewport_width / 2 - button_width / 2), button_y_start + 1 * button_y_spacing],
                           callback=lambda: GUI_manager.change_window(GUI_manager.LIVE_WINDOW))
            dpg.add_button(label="About", width=button_width, height=button_height,
                           pos=[int(viewport_width / 2 - button_width / 2), button_y_start + 2 * button_y_spacing],
                           callback=lambda: GUI_manager.change_window(GUI_manager.LIVE_WINDOW))
            dpg.add_button(label="Exit", width=button_width, height=button_height,
                           pos=[int(viewport_width / 2 - button_width / 2), button_y_start + 3 * button_y_spacing],
                           callback=dpg.stop_dearpygui)

        # Indicate that this window has been created
        self.is_created = True
