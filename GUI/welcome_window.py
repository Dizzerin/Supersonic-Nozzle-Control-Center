import dearpygui.dearpygui as dpg
from Software_Interfaces.window_interface import IWindow
from Software_Interfaces.config_handler_interface import IConfigHandler
from GUI.settings_window import create_settings_pop_window
from GUI import GUI_manager


class WelcomeWindow(IWindow):
    def __init__(self, config_handler: IConfigHandler):
        # Call super class's init
        super(WelcomeWindow, self).__init__()

        # Local vars
        self.is_created = False
        self._settings_window_tag = "settings_window"
        self._config_handler = config_handler

        # TODO (optional) create rounded transparent button style and apply to buttons on this screen

    def is_created(self) -> bool:
        return self.is_created

    def tag(self) -> str:
        return "Welcome Window"

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

        # Create textures/images (which will later be added to the window)
        # width1, height1, channels1, data1 = dpg.load_image(r"Image_Resources/Logo2.png")
        # width2, height2, channels2, data2 = dpg.load_image(r"Image_Resources/Red_Room_Red_Text.png")
        # width2, height2, channels2, data2 = dpg.load_image(r"Image_Resources/Red_Room_Blue_Text.png")
        # width2, height2, channels2, data2 = dpg.load_image(r"Image_Resources/Blue_Room_Blue_Text.png")
        # width2, height2, channels2, data2 = dpg.load_image(r"Image_Resources/Blue_Room_Blue_Text_Lots_Of_Roof.png")
        # width2, height2, channels2, data2 = dpg.load_image(r"Image_Resources/Red_Room_Blue_Text_Lots_Of_Roof.png")
        width2, height2, channels2, data2 = dpg.load_image(r"Image_Resources/Red_Room_Red_Text_Lots_Of_Roof.png")
        with dpg.texture_registry():
            # dpg.add_static_texture(width=width1, height=height1, default_value=data1, tag="title_image")
            dpg.add_static_texture(width=width2, height=height2, default_value=data2, tag="background_image")

        # Build settings popup/modal window
        create_settings_pop_window(self._config_handler, self._settings_window_tag, viewport_width, viewport_height)

        # Build main welcome window
        with dpg.window(tag=self.tag(), show=True):

            # Add background image
            dpg.add_image("background_image", pos=[0, 0])

            # Add buttons
            dpg.add_button(label="Live Session", width=button_width, height=button_height,
                           pos=[int(viewport_width / 2 - button_width / 2), button_y_start + 0 * button_y_spacing],
                           callback=lambda: GUI_manager.change_window(GUI_manager.INITIALIZATION_WINDOW))

            dpg.add_button(label="Settings", width=button_width, height=button_height,
                           pos=[int(viewport_width / 2 - button_width / 2), button_y_start + 1 * button_y_spacing],
                           callback=lambda: dpg.configure_item(self._settings_window_tag, show=True))

            dpg.add_button(label="About", tag="About", width=button_width, height=button_height,
                           pos=[int(viewport_width / 2 - button_width / 2), button_y_start + 2 * button_y_spacing],
                           callback=lambda: GUI_manager.change_window(GUI_manager.ABOUT_WINDOW))

            dpg.add_button(label="Exit", width=button_width, height=button_height,
                           pos=[int(viewport_width / 2 - button_width / 2), button_y_start + 3 * button_y_spacing],
                           callback=dpg.stop_dearpygui)

        # Indicate that this window has been created
        self.is_created = True
