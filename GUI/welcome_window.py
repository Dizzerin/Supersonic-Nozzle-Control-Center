import dearpygui.dearpygui as dpg
from Interfaces.window_interface import IWindow
from Interfaces.config_handler_interface import IConfigHandler
from GUI import GUI_manager
from Temp_Interfaces.custom_types import ADCInput, SettingsObj, ADCMapObj
from typing import List


class WelcomeWindow(IWindow):
    def __init__(self, config_handler: IConfigHandler):
        # Call super class's init
        super(WelcomeWindow, self).__init__()

        # Local vars
        self.is_created = False
        self._settings_window_tag = "settings_window"
        self._config_handler = config_handler

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
        # Local UI element widths
        settings_window_width = 800
        settings_window_height = 500
        settings_combo_box_width = 80
        settings_text_width = 200
        directory_selector_window_width = 800
        directory_selector_window_height = 300

        # Important UI element tags
        default_camera_index_selection_tag = "camera_index_tag"
        camera_width_selection_tag = "camera_width_tag"
        camera_height_selection_tag = "camera_height_tag"
        current_default_save_dir_tag = "current_default_save_dir_tag"
        # Note: all ADC selection combo box tags are set dynamically using the following format
        # tag = pressure_sensor.name.value + "_adc_selection_tag"

        # Read config file
        default_camera = self._config_handler.get_default_camera_index()
        valid_ADC_options = [element.value for element in ADCInput]
        temperature_sensors = self._config_handler.get_temperature_sensors()
        pressure_sensors = self._config_handler.get_pressure_sensors()
        camera_width = self._config_handler.get_camera_width()
        camera_height = self._config_handler.get_camera_height()
        default_save_directory = self._config_handler.get_default_save_directory()

        # Settings
        with dpg.window(label="Settings", tag=self._settings_window_tag, show=False, modal=True,
                        width=settings_window_width, height=settings_window_height,
                        pos=[int(viewport_width / 2 - settings_window_width / 2),
                             int(viewport_height / 2 - settings_window_height / 2)]):
            # Notice at top
            dpg.add_text("Note: None of the changes you make here will be saved until you select \"OK\" at the bottom!",
                         color=(247, 40, 40, 255))

            # Default Camera Setting
            dpg.add_spacer(height=10)
            with dpg.table(header_row=False, resizable=False, borders_innerH=False, borders_outerH=False,
                           borders_innerV=False, borders_outerV=False):
                dpg.add_table_column(init_width_or_weight=settings_text_width, width_fixed=True)
                dpg.add_table_column()

                with dpg.table_row():
                    camera_index_text_tag = dpg.add_text("Default Camera Index:")
                    # Tooltip
                    with dpg.tooltip(parent=camera_index_text_tag):
                        dpg.add_text(
                            "This specifies the default camera to use if multiple cameras are connected to the system. "
                            "If only one camera is connected, use \"Camera 0\".")
                    dpg.add_combo(["Camera " + str(n) for n in range(0, 5)],
                                  default_value="Camera {}".format(default_camera),
                                  width=settings_combo_box_width,
                                  tag=default_camera_index_selection_tag)

            # ADC Input Mappings
            dpg.add_spacer(height=20)
            ADC_text_tag = dpg.add_text("ADC Input Mapping:")
            # Tooltip
            with dpg.tooltip(parent=ADC_text_tag):
                dpg.add_text("This specifies the physical ports on the ADC which the sensors are connected to.")
            with dpg.table(header_row=False, resizable=False, borders_innerH=False, borders_outerH=False,
                           borders_innerV=False, borders_outerV=False):
                dpg.add_table_column(init_width_or_weight=settings_text_width, width_fixed=True)
                dpg.add_table_column()
                # Temperature sensors
                for temperature_sensor in temperature_sensors:
                    with dpg.table_row():
                        dpg.add_text("Temperature Sensor {}:".format(temperature_sensor.name.value[-1]),
                                     tag=temperature_sensor.name.value)
                        # Tooltip
                        with dpg.tooltip(parent=temperature_sensor.name.value):
                            dpg.add_text(temperature_sensor.descr_string)
                        # Combo selection box
                        dpg.add_combo(valid_ADC_options, label="Input",
                                      default_value=temperature_sensor.adc_input.value,
                                      width=settings_combo_box_width,
                                      tag=temperature_sensor.name.value + "_adc_selection_tag")
                # Pressure sensors
                for pressure_sensor in pressure_sensors:
                    with dpg.table_row():
                        dpg.add_text("Pressure Sensor {}:".format(pressure_sensor.name.value[-1]),
                                     tag=pressure_sensor.name.value)
                        # Tooltip
                        with dpg.tooltip(parent=pressure_sensor.name.value):
                            dpg.add_text(pressure_sensor.descr_string)
                        # Combo selection box
                        dpg.add_combo(valid_ADC_options, label="Input",
                                      default_value=pressure_sensor.adc_input.value,
                                      width=settings_combo_box_width,
                                      tag=pressure_sensor.name.value + "_adc_selection_tag")

            # Camera Resolution Settings (Width and Height)
            dpg.add_spacer(height=20)
            dpg.add_text("Camera Resolution:")
            with dpg.group(horizontal=True):
                dpg.add_input_int(tag=camera_width_selection_tag, width=50, step=0, default_value=camera_width)
                dpg.add_text(" x ")
                dpg.add_input_int(tag=camera_height_selection_tag, width=50, step=0, default_value=camera_height)
                dpg.add_text("(width x height)")

            # Default Save Directory Setting
            dpg.add_spacer(height=20)
            default_save_directory_text_tag = dpg.add_text("Default Save Directory:")
            # Tooltip
            with dpg.tooltip(parent=default_save_directory_text_tag):
                dpg.add_text("This specifies the default directory where video recordings and exported data will"
                             "be saved to.")

            with dpg.group(horizontal=True):
                dpg.add_text("Current Directory: ")
                dpg.add_text(default_save_directory, tag=current_default_save_dir_tag)

            # Create Directory Selector Dialog (created hidden, but is shown when the select button is pressed)
            selection_window_tag = dpg.add_file_dialog(label="Select default save directory", tag="select",
                                                       directory_selector=True,
                                                       callback=self._directory_selector_callback,
                                                       user_data=current_default_save_dir_tag,
                                                       width=directory_selector_window_width,
                                                       height=directory_selector_window_height,
                                                       show=False
                                                       )
            dpg.add_button(label="Choose New Directory", tag="open_select_window", height=23,
                           callback=lambda: dpg.configure_item(selection_window_tag, show=True))

            # OK and Cancel buttons
            dpg.add_spacer(height=5)
            dpg.add_separator()
            dpg.add_spacer(height=5)
            with dpg.group(horizontal=True):
                # TODO the get_value call doesn't appear to get the selected value from the combo boxes
                dpg.add_button(label="OK", width=75,
                               callback=self._settings_ok_button_callback,
                               user_data=SettingsObj(
                                   default_camera_index=dpg.get_value(default_camera_index_selection_tag),
                                   camera_width=dpg.get_value(camera_width_selection_tag),
                                   camera_height=dpg.get_value(camera_height_selection_tag),
                                   default_save_location=dpg.get_value(current_default_save_dir_tag),
                                   ADC_map_list=[ADCMapObj(sensor_name=pressure_sensor.name,
                                                           adc_input=ADCInput(dpg.get_value(
                                                               pressure_sensor.name.value + "_adc_selection_tag"))) for
                                                 pressure_sensor in pressure_sensors] +
                                                [ADCMapObj(sensor_name=temperature_sensor.name, adc_input=ADCInput(
                                                    dpg.get_value(
                                                        temperature_sensor.name.value + "_adc_selection_tag"))) for
                                                 temperature_sensor in temperature_sensors]
                               )
                               )
                dpg.add_button(label="Cancel", width=75,
                               callback=lambda: dpg.configure_item(self._settings_window_tag, show=False))

    def _directory_selector_callback(self, sender, app_data, user_data):
        """
        This is called whenever clicks the "OK" button in the file selector dialog window that can be accessed
        from settings (when the user wishes to specify the default save directory for recordings and exported data)

        :param sender: the tag of the UI element (the file selection dialog window)
        :param app_data: (dictionary) -- with lots of stuff in it, just examine it for yourself
        :param user_data: the tag of the current_directory_text
        :return: None
        """
        # print("sender: ", sender)
        # print("app_data: ", app_data)
        # print("user_data: ", user_data)

        selected_directory = app_data['file_path_name']

        # Set the new default directory
        """
        (This doesn't set the save directory on the config handler object because we don't
        want anything to take effect until the user actually clicks "OK")
        
        I have chosen to simply set the value of the current directory text element in the settings window UI here.
        The settings window then passes the value of this text element as part of the SettingsObj which gets passed to
        the OK button callback handler whenever OK is clicked
        """
        # self._user_selected_save_directory = selected_directory
        # self._config_handler.set_default_save_directory(selected_directory)

        # Update the UI element displaying the currently selected directory path
        dpg.set_value(item=user_data, value=selected_directory)

        # Show the settings window again
        dpg.configure_item(self._settings_window_tag, show=True)

    def _settings_ok_button_callback(self, sender, app_data, user_data: SettingsObj):
        """
        This is called when the user clicks the "OK" button at the bottom of the settings window
        We now need to save all the settings

        :param sender: the tag of the UI element (the file selection dialog window)
        :param user_data: SettingsObj (Setting Object)
        :type user_data: SettingsObj
        :return: None
        """
        # Update all basic settings on config handler to reflect the user's selections in the settings window
        self._config_handler.set_default_camera_index(user_data.default_camera_index)
        self._config_handler.set_camera_width(user_data.camera_width)
        self._config_handler.set_camera_height(user_data.camera_height)
        self._config_handler.set_default_save_directory(user_data.default_save_location)

        # Update ADC Input Mappings
        selected_adc_inputs: List[ADCInput] = []  # Running "total" list of all the adc inputs we've encountered so far
        for ADC_map_obj in user_data.ADC_map_list:
            # Make sure this ADC input isn't already mapped to a sensor
            if ADC_map_obj.adc_input in selected_adc_inputs:
                # TODO raise custom exception type instead? or show a popup window with the warning
                raise Exception("ADC Input {} mapped to two sensors!".format(ADCMapObj.adc_input.value))

            else:
                # Set/map the sensor to its ADC input
                self._config_handler.set_adc_input(adc_map_obj=ADC_map_obj)

                # Add ADC input to list of used ADC inputs
                selected_adc_inputs.append(ADC_map_obj.adc_input)

        # Save the new settings
        self._config_handler.write_config_file()

        # Close the settings window
        dpg.configure_item(self._settings_window_tag, show=False)

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
                           callback=lambda: dpg.configure_item(self._settings_window_tag, show=True))

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
