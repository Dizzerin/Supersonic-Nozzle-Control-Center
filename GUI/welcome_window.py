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

        # TODO (skip) create rounded transparent button style and apply to buttons on this screen

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
        # dpg.set_viewport_decorated(self.include_title_bar())
        # dpg.maximize_viewport()
        title_bar_height = 47

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
            dpg.add_static_texture(width=width2, height=height2-title_bar_height, default_value=data2, tag="background_image")

        # Build settings popup/modal window
        create_settings_pop_window(self._config_handler, self._settings_window_tag, viewport_width, viewport_height)

        # Build main welcome window
        with dpg.window(tag=self.tag(), show=True, no_scrollbar=True):

            # Add background image
            dpg.add_image("background_image", pos=[0, 0])

            # Add buttons
            dpg.add_button(label="Live Session", width=button_width, height=button_height,
                           pos=[int(viewport_width / 2 - button_width / 2), button_y_start + 0 * button_y_spacing],
                           callback=lambda: GUI_manager.change_window(GUI_manager.INITIALIZATION_WINDOW))

            dpg.add_button(label="About", tag="About", width=button_width, height=button_height,
                           pos=[int(viewport_width / 2 - button_width / 2), button_y_start + 1 * button_y_spacing],
                           callback=lambda: GUI_manager.change_window(GUI_manager.ABOUT_WINDOW))

            dpg.add_button(label="Exit", width=button_width, height=button_height,
                           pos=[int(viewport_width / 2 - button_width / 2), button_y_start + 2 * button_y_spacing],
                           callback=dpg.stop_dearpygui)

            # TODO (skip) Add settings feature back in
            #   For now I have chosen to simply remove this button so it can't be accessed this way.
            #   In theory you can still directly edit the config.cfg file, but not all of the settings in there are actually used... hence why I am removing the obvious access to modify the settings.
            #   Reasons this was removed:
            #       I didn't implement use of all the settings in the config file yet, for example the default save directory and the camera index settings are not used (among other things probably)
            #       I didn't finish writing the stuff to verify the settings in the config file to make sure its valid all the time etc.
            #       Not all of the settings in the config file are available on the settings screen I created
            #       If we add settings back in, we should add more things to the settings (like being able to adjust the sample rate, camera focus and brightness settings, etc. for example)
            #       I have run out of time to work on this and the settings really aren't necessary, so its easiest to just remove them or remove access to them, which I'm doing by just taking this button away.
            #       If you want to add them back in, uncomment the code below and click the button and see what it does and what's there and then go from there to see what all else needs to be done (there are several other todo's marked optional that are related to settings the the config file stuff)
            # dpg.add_button(label="Settings", width=button_width, height=button_height,
            #                pos=[int(viewport_width / 2 - button_width / 2), button_y_start + 3 * button_y_spacing],
            #                callback=lambda: dpg.configure_item(self._settings_window_tag, show=True))

        # Indicate that this window has been created
        self.is_created = True
