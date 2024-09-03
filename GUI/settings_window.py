import dearpygui.dearpygui as dpg
from Software_Interfaces.config_handler_interface import IConfigHandler
from Custom_Types.custom_types import ConfigSettings, TemperatureSensorConfigData, PressureSensorConfigData, \
    ValidADCInputs
from typing import List, TypedDict


# Classes to strictly specify types to be supplied to callback functions
class _DirSelectorCallbackDict(TypedDict):
    current_dir_text_tag: str
    settings_window_tag: str


class _OKButtonCallbackDict(TypedDict):
    config_handler: IConfigHandler
    settings_window_tag: str
    config_settings_obj: ConfigSettings


def create_settings_pop_window(config_handler: IConfigHandler, settings_window_tag: str, viewport_width: int,
                               viewport_height: int):
    # Local UI element widths
    settings_window_width = 800
    settings_window_height = 500
    warning_window_width = 300
    warning_window_height = 80
    settings_combo_box_width = 80
    settings_text_width = 200
    directory_selector_window_width = 800
    directory_selector_window_height = 300

    # Important UI element tags
    default_camera_index_selection_tag = "camera_index_tag"
    camera_width_selection_tag = "camera_width_tag"
    camera_height_selection_tag = "camera_height_tag"
    current_dir_location_text_tag = "current_dir_location_text_tag"
    warning_popup_tag = "warning_popup_tag"
    warning_popup_text_tag = "warning_popup_text_tag"
    # Note: all ADC selection combo box tags are set dynamically using the following format
    # tag = pressure_sensor.name.value + "_adc_selection_tag"

    # Read config file
    default_camera = config_handler.get_default_camera_index()
    valid_ADC_options = [element.value for element in ValidADCInputs]
    temperature_sensors = config_handler.get_temperature_sensors()
    pressure_sensors = config_handler.get_pressure_sensors()
    camera_width = config_handler.get_camera_width()
    camera_height = config_handler.get_camera_height()
    default_save_directory = config_handler.get_default_save_directory()

    def _settings_ok_button_callback(sender, app_data, user_data: _OKButtonCallbackDict):
        """
        This is called when the user clicks the "OK" button at the bottom of the settings window
        We now need to save all the settings

        :param sender: the tag of the UI element (the file selection dialog window)
        :param app_data: None
        :type app_data: None
        :param user_data: None
        :return: None
        """
        config_settings_obj = ConfigSettings(
            default_camera_index=int(dpg.get_value(default_camera_index_selection_tag)[-1]),
            camera_width=dpg.get_value(camera_width_selection_tag),
            camera_height=dpg.get_value(camera_height_selection_tag),
            default_save_directory=dpg.get_value(current_dir_location_text_tag),
            temperature_sensor_list=[TemperatureSensorConfigData(
                name=temperature_sensor.name,
                descr_string=temperature_sensor.descr_string,
                adc_input=ValidADCInputs(dpg.get_value(temperature_sensor.name + "_adc_selection_tag")),
                amplifier_gain=temperature_sensor.amplifier_gain,
            ) for temperature_sensor in temperature_sensors],
            pressure_sensor_list=[PressureSensorConfigData(
                name=pressure_sensor.name,
                descr_string=pressure_sensor.descr_string,
                adc_input=ValidADCInputs(dpg.get_value(pressure_sensor.name + "_adc_selection_tag")),
                amplifier_gain=pressure_sensor.amplifier_gain,
                sensor_gain=pressure_sensor.sensor_gain,
                sensor_offset=pressure_sensor.sensor_offset,
            ) for pressure_sensor in pressure_sensors]
        )

        # Update all basic settings on config handler to reflect the user's selections in the settings window
        config_handler.set_default_camera_index(config_settings_obj.default_camera_index)
        config_handler.set_camera_width(config_settings_obj.camera_width)
        config_handler.set_camera_height(config_settings_obj.camera_height)
        # TODO we should also verify these things on startup?  Or before trying to write to it at least
        # TODO could do more verifications on this to make sure this directory exists etc.
        #   Also remember we can use the warning_window_tag
        #   window and its warning_window_text to show the error status to the user (see what we do below in the event
        #   of an ADC input mapped to two sensors.
        config_handler.set_default_save_directory(config_settings_obj.default_save_directory)

        # Verify one ADC input isn't mapped to two different sensors
        used_ADC_inputs: List[
            ValidADCInputs] = []  # Running "total" list of all the adc inputs we've encountered so far
        # Loop through all pressure sensors
        for temperature_sensor in config_settings_obj.temperature_sensor_list:
            # Throw error if this ADC input isn't already mapped to a sensor
            if temperature_sensor.adc_input in used_ADC_inputs:
                # ERROR: ADC input mapped to two sensors!
                # Show popup with warning and edit text contents of window
                dpg.set_value(warning_popup_text_tag,
                              "ADC Input: \"{}\" mapped to two sensors!".format(temperature_sensor.adc_input.value) +
                              "\r\nPlease correct this and try again.")
                dpg.configure_item(warning_popup_tag, show=True)
                return  # Don't save the data!
            # Else add ADC input to list of used ADC inputs
            else:
                used_ADC_inputs.append(temperature_sensor.adc_input)

        # Loop through all temperature sensors
        for pressure_sensor in config_settings_obj.pressure_sensor_list:
            # Throw error if this ADC input isn't already mapped to a sensor
            if pressure_sensor.adc_input in used_ADC_inputs:
                # ERROR: ADC input mapped to two sensors!
                # Show popup with warning and edit text contents of window
                dpg.set_value(warning_popup_text_tag,
                              "ADC Input: \"{}\" mapped to two sensors!".format(pressure_sensor.adc_input.value) +
                              "\r\nPlease correct this and try again.")
                dpg.configure_item(warning_popup_tag, show=True)
                return  # Don't save the data!
            # Else add ADC input to list of used ADC inputs
            else:
                used_ADC_inputs.append(pressure_sensor.adc_input)

        # Update all the temperature sensors
        for temperature_sensor in config_settings_obj.temperature_sensor_list:
            config_handler.set_temperature_sensor(temperature_sensor)

        # Update all the pressure sensors
        for pressure_sensor in config_settings_obj.pressure_sensor_list:
            config_handler.set_pressure_sensor(pressure_sensor)

        # Save the new settings
        config_handler.write_config_file()

        # Close the settings window
        dpg.configure_item(settings_window_tag, show=False)

    # Create popup that can be used for warnings (hidden by default)
    with dpg.window(label="Error!", modal=True, show=False, tag=warning_popup_tag,
                    width=warning_window_width, height=warning_window_height,
                    pos=[int(viewport_width / 2 - warning_window_width / 2),
                         int(viewport_height / 2 - warning_window_height / 2)]):
        dpg.add_text("Unknown error", tag=warning_popup_text_tag)
        dpg.add_spacer()
        dpg.add_button(label="OK",
                       pos=[warning_window_width / 2 - 15, warning_window_height - 10],
                       callback=lambda: dpg.configure_item(warning_popup_tag, show=False))

    # Create Settings GUI Window
    with dpg.window(label="Settings", tag=settings_window_tag, show=False,
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
                    dpg.add_text("Temperature Sensor {}:".format(temperature_sensor.name[-1]),
                                 tag=temperature_sensor.name)
                    # Tooltip
                    with dpg.tooltip(parent=temperature_sensor.name):
                        dpg.add_text(temperature_sensor.descr_string)
                    # Combo selection box
                    dpg.add_combo(valid_ADC_options, label="Input",
                                  default_value=temperature_sensor.adc_input.value,
                                  width=settings_combo_box_width,
                                  tag=temperature_sensor.name + "_adc_selection_tag")
            # Pressure sensors
            for pressure_sensor in pressure_sensors:
                with dpg.table_row():
                    dpg.add_text("Pressure Sensor {}:".format(pressure_sensor.name[-1]),
                                 tag=pressure_sensor.name)
                    # Tooltip
                    with dpg.tooltip(parent=pressure_sensor.name):
                        dpg.add_text(pressure_sensor.descr_string)
                    # Combo selection box
                    dpg.add_combo(valid_ADC_options, label="Input",
                                  default_value=pressure_sensor.adc_input.value,
                                  width=settings_combo_box_width,
                                  tag=pressure_sensor.name + "_adc_selection_tag")

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
            dpg.add_text("This specifies the default directory where and exported data will be saved to.")

        with dpg.group(horizontal=True):
            dpg.add_text("Current Directory: ")
            dpg.add_text(default_save_directory, tag=current_dir_location_text_tag)

        # Create Directory Selector Dialog (created hidden, but is shown when the select button is pressed)
        selection_window_tag = dpg.add_file_dialog(label="Select default save directory", tag="select",
                                                   directory_selector=True,
                                                   callback=_directory_selector_callback,
                                                   user_data={"current_dir_text_tag": current_dir_location_text_tag,
                                                              "settings_window_tag": settings_window_tag},
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
            # OK button callback user data contains all settings data that gets passed to the configHandler
            dpg.add_button(label="OK", width=75, callback=_settings_ok_button_callback)
            dpg.add_button(label="Cancel", width=75,
                           callback=lambda: dpg.configure_item(settings_window_tag, show=False))


def _directory_selector_callback(sender, app_data, user_data: _DirSelectorCallbackDict):
    """
    This is called whenever clicks the "OK" button in the file selector dialog window that can be accessed
    from settings (when the user wishes to specify the default save directory for data logging)

    :param sender: the tag of the UI element (the file selection dialog window)
    :param app_data: (dictionary) -- with lots of stuff in it, just examine it for yourself
    :type app_data: dict
    :param user_data: (dictionary) -- contains the settings window tag and the current_dir_location_text_tag
    :type user_data: _DirSelectorCallbackDict
    :return: None

    Note: There is also a dpg.get_file_dialog_info function that might be interesting to look into
    """
    # Unpack/alias values from user_data and app_data
    current_dir_location_text_tag = user_data["current_dir_text_tag"]
    settings_window_tag = user_data["settings_window_tag"]
    selected_directory = app_data['file_path_name']

    # Set the new default directory
    """
    (This doesn't set the save directory on the config handler object because we don't
    want anything to take effect until the user actually clicks "OK")

    I have chosen to simply set the value of the current directory text element in the settings window UI here.
    The settings window then passes the value of this text element as part of the ConfigSettings object which gets passed to
    the OK button callback handler whenever OK is clicked
    """
    # self._user_selected_save_directory = selected_directory
    # self._config_handler.set_default_save_directory(selected_directory)

    # Update the UI element displaying the currently selected directory path
    dpg.set_value(item=current_dir_location_text_tag, value=selected_directory)

    # Show the settings window again
    dpg.configure_item(settings_window_tag, show=True)
