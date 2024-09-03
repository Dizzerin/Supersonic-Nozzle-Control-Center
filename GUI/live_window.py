import os
import dearpygui.dearpygui as dpg
from Software_Interfaces.window_interface import IWindow
from Hardware_Interfaces.ADC_data_provider_interface import IADCDataProvider
from Hardware_Interfaces.ADC_data_writer_interface import IADCDataWriter
from Hardware_Interfaces.camera_data_provider_interface import ICameraDataProvider
from datetime import datetime
from GUI import GUI_manager


class LiveWindow(IWindow):
    def __init__(self, camera_data_provider: ICameraDataProvider, ADC_data_provider: IADCDataProvider,
                 ADC_data_writer: IADCDataWriter):
        # Call super class's init
        super(LiveWindow, self).__init__()

        # Local vars
        self.cam = camera_data_provider
        self.ADC_data_provider = ADC_data_provider
        self.ADC_data_writer_class = ADC_data_writer
        self.ADC_data_writer = None
        self.logging_in_progress = False

        # TODO change the way this is handled? -- if changing, may also need to change the reset_plots method
        # TODO only store the amount of data necessary for display (so it doesn't continually increase memory consumption)
        # TODO auto rescale graph's y-axes?
        # Plot sizing and data arrays
        # Global pressures and other plot data
        self.time_data = [0]
        self.axis_duration = 200
        self.axis_start_time = 0
        self.axis_end_time = self.axis_duration
        self.num_pressure_plots = 5
        self.plot_height = 150  # pixels
        self.plot_width = 700  # pixels
        self.t0_y_data = []
        self.p0_y_data = []
        self.p1_y_data = []
        self.p2_y_data = []
        self.p3_y_data = []
        self.p4_y_data = []
        self.is_created = False

        # Other sizing vars
        self.directory_selector_window_width = 800
        self.directory_selector_window_height = 300

        # UI element tags
        self.video_texture_tag = "texture_tag"
        self.focus_slider_tag = "focus_slider_tag"
        self.AF_enable_button_tag = "AF_enable_button_tag"
        self.brightness_slider_tag = "brightness_slider_tag"
        self.reset_brightness_tag = "reset_brightness"
        self.logging_button_tag = "logging_button"
        self.logging_status_label_tag = "logging_status_label_tag"
        self.calibrate_button_tag = "calibrate_button"
        self.calibration_status_label_tag = "calibration_status_label"
        self.time_text_box_tag = "time_text_box_tag"
        self.directory_selector_tag = "directory_selector_tag"
        self.dir_location_text_tag = "dir_location_text_tag"

    # Called whenever switching to this screen
    def show(self):
        # Reset camera focus settings (enable autofocus) and brightness settings
        self.cam.reset_all_brightness_and_focus_settings(self.focus_slider_tag, self.AF_enable_button_tag,
                                                         self.brightness_slider_tag)
        # Reset plots and plot values and data
        self._reset_plots()

        # Call super class's show function
        super(LiveWindow, self).show()

    # Called whenever switching away from this screen to another one
    def hide(self):
        # TODO more cleanup tasks when leaving this screen? Stop things etc.? Stop logging? etc.?
        self.logging_in_progress = False
        # Call super class's hide function
        super(LiveWindow, self).hide()

    def is_created(self) -> bool:
        return self.is_created

    def tag(self) -> str:
        return "Live Window"

    def include_title_bar(self) -> bool:
        return True

    def _logging_button_callback(self, sender, data, user_data):
        # TODO note that the calibration is not setup and the conversion stuff is probably
        #   right but hasn't been verified.

        # If not logging...
        if not self.logging_in_progress:
            # Show directory selector dialog (open to default directory)
            dpg.configure_item(self.directory_selector_tag, show=True)
            # Update default filename with current time
            dpg.configure_item(self.directory_selector_tag, default_filename="Recorded Data {}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))  # Suggest default filename with year month day hour minute second
            # Note: The selected directory is set via the _directory_selector_callback2() which in turn calls
            # the _start_logging method once it gets the filepath to save the logged data to.

        # Else if logging already... stop logging
        else:
            # Set flag indicating we are not logging
            self.logging_in_progress = False
            # Reset selected path
            _user_selected_filepath = None
            # Save file
            self.ADC_data_writer.save_file()
            # Change the text on the logging button to start logging
            dpg.configure_item(self.logging_button_tag, label="Start Logging")
            dpg.set_value(self.logging_status_label_tag, "Status: Not logging")
            # Clear the ADC data writer object since we are done with it and will want to create a new one if we want to start logging again
            self.ADC_data_writer = None

    def start_logging(self, filepath):
        # Create new data logger object
        self.ADC_data_writer = self.ADC_data_writer_class(filepath)

        # Start logging
        # Set logging start time
        self.ADC_data_writer.set_logging_start_time()
        # Set flag indicating we are logging
        self.logging_in_progress = True
        # Change the text on the logging button to stop logging
        dpg.configure_item(self.logging_button_tag, label="Stop Logging")
        dpg.set_value(self.logging_status_label_tag, "Status: Logging")

    def _update_video(self):
        raw_data = self.cam.get_next_frame()
        dpg.set_value(self.video_texture_tag, raw_data)

    def _update_plot(self, series_tag, x_axis_tag, text_box_tag, y_data):
        # "Scroll" x-axis
        dpg.set_axis_limits(x_axis_tag, self.axis_start_time, self.axis_end_time)

        # Update axis data
        dpg.set_value(series_tag, [self.time_data, y_data])

        # Update text box displaying current value
        current_label = dpg.get_value(
            text_box_tag)  # Capture the current text string (something like: "P0: -00.000 (psi)")
        numeric_start_index = current_label.find(": ") + 1
        numeric_end_index = current_label.rfind(" (")
        # Update only the numeric portion of the string (with the latest measurement value) and retain the rest of the string
        dpg.set_value(text_box_tag,
                      current_label[:numeric_start_index + 1] + "{:#8.3f}".format(y_data[-1]) + current_label[
                                                                                                numeric_end_index:])

    def _update_plots(self):
        # Update time and pressure and temperature values
        self.time_data.append(self.time_data[-1] + 1)
        if len(self.time_data) >= self.axis_end_time:
            self.axis_start_time += 1
            self.axis_end_time += 1
        dpg.set_value(self.time_text_box_tag, "Time: {:#6.3f} (s)".format(self.time_data[-1]))

        # Read new data from ADC
        ADC_data = self.ADC_data_provider.get_next_data_row()
        self.t0_y_data.append(ADC_data.t0)
        self.p0_y_data.append(ADC_data.p0)
        self.p1_y_data.append(ADC_data.p1)
        self.p2_y_data.append(ADC_data.p2)
        self.p3_y_data.append(ADC_data.p3)
        self.p4_y_data.append(ADC_data.p4)

        # Update plots
        self._update_plot("t0_series", "t0_x_axis", "t0_text_box", self.t0_y_data)
        self._update_plot("p0_series", "p0_x_axis", "p0_text_box", self.p0_y_data)
        self._update_plot("p1_series", "p1_x_axis", "p1_text_box", self.p1_y_data)
        self._update_plot("p2_series", "p2_x_axis", "p2_text_box", self.p2_y_data)
        self._update_plot("p3_series", "p3_x_axis", "p3_text_box", self.p3_y_data)
        self._update_plot("p4_series", "p4_x_axis", "p4_text_box", self.p4_y_data)

    def _reset_plots(self):
        # Reset plot data
        self.time_data = [0]
        self.axis_start_time = 0
        self.axis_end_time = self.axis_duration
        self.t0_y_data = []
        self.p0_y_data = []
        self.p1_y_data = []
        self.p2_y_data = []
        self.p3_y_data = []
        self.p4_y_data = []
        self._update_plots()

    def update(self):
        self._update_video()
        self._update_plots()

        # Write new data row if logging is in progress
        # TODO THIS SHOULD BE DONE DIFFERENT
        #   Should use the same data that was placed on the graphs -- should probably also slow this down?
        #   also want to be able to adjust the sampling rate
        if self.logging_in_progress:
            # Write new logging line
            last_sample_time = datetime.now()
            self.ADC_data_writer.write_ADC_data(self.ADC_data_provider.get_next_data_row(), last_sample_time)

    def create(self, viewport_width: int, viewport_height: int):
        # Local vars
        raw_data = self.cam.get_next_frame()

        # Create textures which will later be added to the window
        with dpg.texture_registry(show=False):
            dpg.add_raw_texture(self.cam.get_width(), self.cam.get_height(), raw_data, format=dpg.mvFormat_Float_rgba,
                                tag=self.video_texture_tag)

        # Build the window
        with dpg.window(tag=self.tag(), show=False):
            dpg.add_button(label="Home", callback=lambda: GUI_manager.change_window(GUI_manager.WELCOME_WINDOW))

            # Master group to divide window into two columns
            with dpg.group(horizontal=True) as master_group:
                # Left-hand side group
                with dpg.group(horizontal=False) as left_group:
                    # Video feed
                    dpg.add_image(self.video_texture_tag)

                    # Autofocus checkbox
                    with dpg.group(horizontal=True):
                        dpg.add_checkbox(label="Auto Focus", default_value=True,
                                         user_data=self.focus_slider_tag,
                                         callback=self.cam.set_autofocus_callback, tag=self.AF_enable_button_tag)
                        # dpg.add_checkbox(label="Auto Exposure")

                    with dpg.group(horizontal=True):
                        # Focus and brightness sliders
                        slider_and_button_width = 150
                        with dpg.group(horizontal=False):
                            # Todo Verify range
                            dpg.add_slider_int(label="Focus", tag=self.focus_slider_tag, vertical=False,
                                               default_value=0,
                                               min_value=0,
                                               max_value=1012,
                                               clamped=True, width=slider_and_button_width,
                                               user_data=self.AF_enable_button_tag,
                                               callback=self.cam.set_focus_callback)
                            dpg.add_slider_int(label="Brightness", tag=self.brightness_slider_tag, vertical=False,
                                               default_value=0,
                                               min_value=-64,
                                               max_value=64, width=slider_and_button_width, clamped=True,
                                               callback=self.cam.set_brightness_callback)
                            dpg.add_spacer(height=5)
                            dpg.add_button(label="Reset brightness", tag=self.reset_brightness_tag,
                                           width=slider_and_button_width,
                                           user_data=self.brightness_slider_tag,
                                           callback=self.cam.reset_brightness_callback)

                        # Logging and Calibration Buttons
                        button_width = 150
                        button_height = 35
                        with dpg.group(horizontal=True):
                            dpg.add_spacer(width=100)
                            # Left column (calibration)
                            with dpg.group(horizontal=False):
                                dpg.add_text("Calibration")  # Header
                                dpg.add_spacer(height=20)
                                dpg.add_text("Status: Uncalibrated", tag=self.calibration_status_label_tag) # TODO update this
                                dpg.add_spacer(height=10)
                                dpg.add_text("Atmospheric Pressure (PSI):")
                                dpg.add_input_float(tag="atmospheric_pressure_input", width=button_width, step=0.01,
                                                    min_value=0.0, max_value=1000.0)
                                # # TODO Set callback
                                dpg.add_button(label="Calibrate Sensors", width=button_width, height=button_height,
                                               tag=self.calibrate_button_tag)
                                                # callback = self._calibration_button_callback)
                            dpg.add_spacer(width=100)
                            # Right column (Logging)
                            with dpg.group(horizontal=False):
                                dpg.add_text("Logging")  # Header
                                dpg.add_spacer(height=20)
                                dpg.add_text("Status: Not logging", tag=self.logging_status_label_tag) # TODO update this
                                dpg.add_spacer(height=10)
                                dpg.add_button(label="Start Logging", width=button_width, height=button_height,
                                               tag=self.logging_button_tag,
                                               callback=self._logging_button_callback)

                # Right-hand side group
                # with dpg.group(horizontal=True, pos=[viewport_width // 2 + 80, 60]) as right_group:
                with dpg.group(horizontal=True) as right_group:
                    # Heading text for graphs
                    dpg.add_text("Live Data", pos=[viewport_width // 2 + viewport_width // 4, 30])
                    # Add plots
                    with dpg.group(horizontal=False, pos=[viewport_width // 2 + 80, 60]) as plot_group:
                        with dpg.subplots(rows=self.num_pressure_plots + 1, columns=1, row_ratios=[1, 1, 1, 1, 1, 1.3],
                                          width=self.plot_width,
                                          height=((self.num_pressure_plots + 1) * self.plot_height + 10)) as plot_group:
                            # Create pressure plots (and temperature plot at the end)
                            """
                            Create num_plots pressure subplots all with the following format
                                plot label: p#_plot
                                x-axis label: p#_x_axis
                                y-axis label: p#_y_axis
                                line series label: "Pressure #"
                                line series tag: p#_series
                                plot text box tag: p#_text_box    <-- this text box is meant to be used to show the live reading value
                            Where # is 0 up to num_plots

                            Note:
                                Each graph's y-axis series data must be set after this function creates all the graphs

                                Also the labels the series data can be updated to be more meaningful than "Pressure #"

                                A final temperature plot is created separately at the end, this is partly because its name etc.
                                is unique, but also because this plot's x-axis is shown (the others are hidden) in the way
                                the last plot's x-axis is visually shared by all the plots.

                                The row_ratios argument allows the last plot to take up more of the space, this is done because
                                the last plot's x-axis includes labels, so the plot area is shrunk.  The ratios currently set to
                                make all plot areas appear equal
                            """
                            # TODO set each plot's y axis limits?
                            # Create pressure plots
                            for i in range(self.num_pressure_plots):
                                # Add plot
                                with dpg.plot(label="p{}_plot".format(str(i)), no_title=True, no_menus=True):
                                    # Create legend
                                    dpg.add_plot_legend()
                                    # Create x and y axes
                                    dpg.add_plot_axis(dpg.mvXAxis, label="", tag="p{}_x_axis".format(str(i)),
                                                      no_tick_labels=True)
                                    with dpg.plot_axis(dpg.mvYAxis, label="(psi)", tag="p{}_y_axis".format(str(i))):
                                        # Create line_series plots
                                        dpg.add_line_series(self.time_data, [], label="Pressure {}".format(str(i)),
                                                            tag="p{}_series".format(str(i)))

                            # Create temperature plot
                            with dpg.plot(label="t0_plot", no_title=True, no_menus=True):
                                # Create legend
                                dpg.add_plot_legend()
                                # Create x and y axes
                                # NOTE: This x-axis is visually shared with all the pressure graphs above!
                                dpg.add_plot_axis(dpg.mvXAxis, label="time (s)", tag="t0_x_axis")
                                with dpg.plot_axis(dpg.mvYAxis, label="(Kelvin)", tag="t0_y_axis"):
                                    # Create line_series plots
                                    dpg.add_line_series(self.time_data, [], label="Temperature 0", tag="t0_series")

                    # Make "Live Data" label/title of the plot group look nicer
                    #   Set PlotPadding to 7 and LabelPadding to 11
                    # TODO figure out why this theme isn't applying to the plot_group
                    #   Or maybe just add a text label and set its properties instead of adjusting all plots in the group
                    with dpg.theme() as plot_group_container_theme:
                        with dpg.theme_component():
                            dpg.add_theme_style(dpg.mvPlotStyleVar_PlotPadding, 10)
                            dpg.add_theme_style(dpg.mvPlotStyleVar_LabelPadding, 10)
                    dpg.bind_item_theme(plot_group, plot_group_container_theme)

                    # TODO Apply a theme to these to make them nicer, maybe a light background and border?
                    # Now add the text boxes next to the plots with their current values
                    with dpg.group(horizontal=False) as label_group:
                        # Create text boxes for pressure plots
                        for i in range(self.num_pressure_plots):
                            dpg.add_text("P{}: {:#8.3f} (psi)".format(i, 0.0), tag="p{}_text_box".format(str(i)),
                                         pos=[viewport_width // 2 + 90 + self.plot_width,
                                              55 + self.plot_height // 2 + ((self.plot_height - 8) * i)])

                        # TODO is it C or Kelvin? -- Change everywhere
                        # Create text boxes for temperature plot
                        dpg.add_text("T0: {:#8.3f} (kelvin)".format(0.0), tag="t0_text_box",
                                     pos=[viewport_width // 2 + 90 + self.plot_width,
                                          60 + self.plot_height // 2 + (
                                                      (self.plot_height - 8) * self.num_pressure_plots)])

                        # Αdd time text box
                        dpg.add_text("Time: {:#6.3f} (s)".format(0.0), tag=self.time_text_box_tag,
                                     pos=[viewport_width // 2 + 90 + self.plot_width,
                                          60 + ((self.plot_height - 5) * (self.num_pressure_plots + 1))])

                    # Add tooltips to temperature and pressure plots and text boxes
                    # TODO use this from config file
                    descriptions = {"t0_y_axis": "Temperature inside the tank (stagnation temperature)",
                                    "p0_y_axis": "Pressure inside the tank (stagnation pressure)",
                                    "p1_y_axis": "Pressure upstream of the throat",
                                    "p2_y_axis": "Pressure at the throat",
                                    "p3_y_axis": "Pressure just downstream of the throat",
                                    "p4_y_axis": "Pressure just upstream of the exit",
                                    "t0_text_box": "Temperature inside the tank (stagnation temperature)",
                                    "p0_text_box": "Pressure inside the tank (stagnation pressure)",
                                    "p1_text_box": "Pressure upstream of the throat",
                                    "p2_text_box": "Pressure at the throat",
                                    "p3_text_box": "Pressure just downstream of the throat",
                                    "p4_text_box": "Pressure just upstream of the exit",
                                    self.time_text_box_tag: "Elapsed time"
                                    }
                    for key, value in descriptions.items():
                        with dpg.tooltip(parent=key):
                            dpg.add_text(value)

            # Create Directory Selector Dialog (created hidden, but is shown when the select button is pressed)
            dpg.add_file_dialog(label="Select save directory", tag=self.directory_selector_tag,
                                directory_selector=False,
                                callback=self._directory_selector_callback2,
                                width=self.directory_selector_window_width,
                                height=self.directory_selector_window_height,
                                modal=True,
                                default_filename="Recorded Data {}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")),   # Suggest default filename with year month day hour minute second
                                show=False
                                )

        # Set ADC's data acquisition start time
        self.ADC_data_provider.set_acquisition_start_time()

        # Indicate that this window has been created
        self.is_created = True

    def _show_confirmation_window(self, file_path):
        # Determine viewport size
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()

        # Window size
        window_width = 200
        window_height = 120

        # Calculate center position
        x_position = (viewport_width - window_width) // 2
        y_position = (viewport_height - window_height) // 2

        def on_yes(sender, app_data):
            # Delete the existing file
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                    print(f"File '{file_path}' has been deleted (overwriting file).")
                except Exception as e:
                    print(f"An error occurred while deleting the file: {e}")
            else:
                print(f"The file '{file_path}' does not exist.")

            # Start logging
            self.start_logging(file_path)

            # Get rid of confirmation window
            dpg.delete_item("Confirmation Window")

        def on_no(sender, app_data):
            # Don't start logging, instead show the file directory selector again
            # Show directory selector dialog (open to default directory)
            dpg.configure_item(self.directory_selector_tag, show=True)
            # Note: The selected directory is set via the _directory_selector_callback2() which in turn calls
            # the _start_logging method once it gets the filepath to save the logged data to.

            # Get rid of confirmation window
            dpg.delete_item("Confirmation Window")

        with dpg.window(
                label="Overwrite Confirmation",
                tag="Confirmation Window",
                no_close=True,
                # modal=True,   # TODO (optional) this makes the window not show at all, maybe because the window just before this is modal and you can only have one modal window at a time or something?  Idk...
                width=window_width,
                height=window_height,
                pos=(x_position, y_position)  # Center the window
        ):
            dpg.add_text(f"The file '{os.path.basename(file_path)}' already exists. Do you want to overwrite it?",
                         wrap=window_width - 20)  # Wrap text with some padding
            with dpg.group(horizontal=True):
                dpg.add_button(label="Yes", width=75, user_data=file_path, callback=on_yes)
                dpg.add_button(label="No", width=75, user_data=file_path, callback=on_no)

    def _directory_selector_callback2(self, sender, app_data):
        """
        This is called whenever clicks the "OK" button in the file selector dialog window
        (when the user wishes to specify the default save location for logged data)

        :param sender: the tag of the UI element (the file selection dialog window)
        :param app_data: (dictionary) -- with lots of stuff in it, just examine it for yourself
        :type app_data: dict
        :return: None

        Note: There is also a dpg.get_file_dialog_info function that might be interesting to look into
        """
        # Unpack/alias values from user_data and app_data
        # The selected directory is the full filepath and filename with spaces (but no file extension yet)
        selected_filename_and_path = app_data['file_path_name']

        # Extract the directory path from the given file path
        directory_path = os.path.dirname(selected_filename_and_path)

        # Check if the directory exists
        if not os.path.exists(directory_path):
            # If it doesn't exist, create it
            os.makedirs(directory_path)

        # If the file already exists, display warning to user and ask if they want to overwrite it
        if os.path.isfile(selected_filename_and_path + ".csv"):
            print("File already exists, asking user if they want to overwrite it")
            self._show_confirmation_window(selected_filename_and_path + ".csv")
            # (In this case the user will click either yes or no on the confirmation window and if they click yes we will then call self.start_logging in another callback)
        else:
            self.start_logging(selected_filename_and_path)

