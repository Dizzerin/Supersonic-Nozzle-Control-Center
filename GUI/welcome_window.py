import dearpygui.dearpygui as dpg
from Interfaces.window_interface import IWindow
from GUI import GUI_manager


class WelcomeWindow(IWindow):
    def __init__(self):
        # Call super class's init
        super(WelcomeWindow, self).__init__()

        # Local vars
        self.is_created = False
        self.settings_window_tag = "settings_window"

        # TODO create rounded transparent button style and apply to buttons on this screen

    def is_created(self) -> bool:
        return self.is_created

    def tag(self) -> str:
        return "Welcome Window"

    def include_title_bar(self) -> bool:
        return False

    def update(self):
        pass

    def _create_settings_pop_window(self, viewport_width: int, viewport_height: int):
        # TODO make this read defaults from config file and write to config file

        settings_window_width = 500
        settings_window_height = 500
        settings_combo_box_width = 80
        settings_text_width = 200
        # Todo (move this somewhere else?)
        with dpg.window(label="Settings", tag=self.settings_window_tag, show=False, modal=True,
                        width=settings_window_width, height=settings_window_height,
                        pos=[int(viewport_width / 2 - settings_window_width / 2),
                             int(viewport_height / 2 - settings_window_height / 2)]):
            # Settings
            with dpg.table(header_row=False, resizable=False, borders_innerH=False, borders_outerH=False,
                           borders_innerV=False, borders_outerV=False):
                dpg.add_table_column(init_width_or_weight=settings_text_width, width_fixed=True)
                dpg.add_table_column()

                with dpg.table_row():
                    dpg.add_text("Default Camera Index:")
                    dpg.add_combo(["Camera " + str(n) for n in range(0, 5)], default_value="Camera 0",
                                  width=settings_combo_box_width)

            dpg.add_spacer(height=20)
            dpg.add_text("ADC Input Mapping:")
            with dpg.table(header_row=False, resizable=False, borders_innerH=False, borders_outerH=False,
                           borders_innerV=False, borders_outerV=False):
                dpg.add_table_column(init_width_or_weight=settings_text_width, width_fixed=True)
                dpg.add_table_column()
                # Todo make sure the same ADC input isn't selected for multiple things (handle in callback? or on "OK")
                #   Load defaults from config file
                #   Save results to config file
                with dpg.table_row():
                    dpg.add_text("Temperature 0:", tag="t0")
                    dpg.add_combo(["ADC" + str(n) for n in range(0, 11)], label="Input",
                                  default_value="ADC0",
                                  width=settings_combo_box_width)
                for i in range(0, 5):
                    with dpg.table_row():
                        dpg.add_text("Pressure {}:".format(i), tag="p{}".format(i))
                        dpg.add_combo(["ADC" + str(n) for n in range(0, 11)], label="Input",
                                      default_value="ADC{}".format(i+1),
                                      width=settings_combo_box_width)

                # Add tooltips to temperature and pressure text
                # plot_tags = ["t0", "p0", "p1", "p2", "p3", "p4"]
                descriptions = {"t0": "Temperature inside the tank (stagnation temperature)",
                                "p0": "Pressure inside the tank (stagnation pressure)",
                                "p1": "Pressure upstream of the throat",
                                "p2": "Pressure at the throat",
                                "p3": "Pressure just downstream of the throat",
                                "p4": "Pressure just upstream of the exit"
                                }
                for key, value in descriptions.items():
                    with dpg.tooltip(parent=key):
                        dpg.add_text(value)

            dpg.add_spacer(height=20)
            dpg.add_text("Welcome Screen Background:")
            # Todo actually implement this, maybe show available images and make them clickable etc.
            dpg.add_combo(["Background " + str(n) for n in range(0, 4)], default_value="Background 1", width=120)

            dpg.add_spacer(height=20)
            dpg.add_text("Camera Resolution:")
            with dpg.group(horizontal=True):
                dpg.add_input_int(tag="width", width=50, step=0, default_value=800)
                dpg.add_text(" x ")
                dpg.add_input_int(tag="height", width=50, step=0, default_value=640)
                dpg.add_text("(width x height)")

            dpg.add_spacer(height=20)
            dpg.add_text("Default Save Location:")
            dpg.add_file_dialog(label="Select default save location", tag="select", show=False)
            dpg.add_button(label="Select", tag="open_select_window", callback=lambda: dpg.configure_item("select", show=True))

            # OK (and Cancel?) buttons
            # Todo actually implement OK and cancel buttons, cancel doesn't save changes, OK does (also do error checking etc.)
            dpg.add_spacer(height=10)
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_button(label="OK", width=75,
                               callback=lambda: dpg.configure_item(self.settings_window_tag, show=False))
                dpg.add_button(label="Cancel", width=75,
                               callback=lambda: dpg.configure_item(self.settings_window_tag, show=False))


    def create(self, viewport_width: int, viewport_height: int):
        # Don't show title bar
        dpg.set_viewport_decorated(self.include_title_bar())
        dpg.maximize_viewport()

        # Local vars
        # Note: These are only used for the button on this screen
        # Todo maybe implement some of this as a style and make the text larger and apply the style to these buttons instead
        button_y_start = viewport_height / 2 + 60
        button_width = 150
        button_height = 35
        button_y_spacing = 60  # Number of vertical pixels between top of one button to top of next only for Welcome Window buttons

        # Title positioning
        title_y_start = 100

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
        self._create_settings_pop_window(viewport_width, viewport_height)

        # Build main welcome window
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
                           callback=lambda: dpg.configure_item(self.settings_window_tag, show=True))

            dpg.add_button(label="About", tag="About", width=button_width, height=button_height,
                           pos=[int(viewport_width / 2 - button_width / 2), button_y_start + 2 * button_y_spacing],
                           callback=lambda: GUI_manager.change_window(GUI_manager.LIVE_WINDOW))
            with dpg.tooltip(parent="About"):
                dpg.add_text("Made By: Caleb Nelson")
                dpg.add_text("Full about page coming later")

            dpg.add_button(label="Exit", width=button_width, height=button_height,
                           pos=[int(viewport_width / 2 - button_width / 2), button_y_start + 3 * button_y_spacing],
                           callback=dpg.stop_dearpygui)

        # Indicate that this window has been created
        self.is_created = True
