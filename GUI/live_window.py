import dearpygui.dearpygui as dpg
from Interfaces.window_interface import IWindow
from Interfaces.ADC_data_provider_interface import IADCDataProvider
from Interfaces.camera_data_provider_interface import ICameraDataProvider
from GUI import GUI_manager


class LiveWindow(IWindow):
    def __init__(self, camera_data_provider: ICameraDataProvider, ADC_data_provider: IADCDataProvider):
        # Call super class's init
        super(LiveWindow, self).__init__()

        # Local vars
        self.cam = camera_data_provider
        self.ADC = ADC_data_provider

        # TODO change the way this is handled?
        # Plot sizing and data arrays
        # Global pressures and other plot data
        self.time_data = [0]
        self.axis_start_time = 0
        self.axis_end_time = 200
        self.num_pressure_plots = 5
        self.plot_height = 150  # pixels
        self.plot_width = 800  # pixels
        self.p0_y_data = []
        self.p1_y_data = []
        self.p2_y_data = []
        self.p3_y_data = []
        self.p4_y_data = []
        self.t0_y_data = []
        self.is_created = False

        # UI element tags
        self.video_texture_tag = "texture_tag"
        self.focus_slider_tag = "focus_slider_tag"
        self.AF_enable_button_tag = "AF_enable_button_tag"
        self.brightness_slider_tag = "brightness_slider_tag"
        self.reset_brightness_tag = "reset_brightness"
        self.recording_button_tag = "recording_button"
        self.calibrate_button_tag = "calibrate_button"

    def is_created(self) -> bool:
        return self.is_created

    def tag(self) -> str:
        return "Live Window"

    def include_title_bar(self) -> bool:
        return True

    def _update_video(self):
        raw_data = self.cam.get_next_frame()
        dpg.set_value(self.video_texture_tag, raw_data)

    def _update_plot(self, series_tag, x_axis_tag, y_data):
        # "Scroll" x-axis
        dpg.set_axis_limits(x_axis_tag, self.axis_start_time, self.axis_end_time)

        # Update axis data
        dpg.set_value(series_tag, [self.time_data, y_data])

    def _update_plots(self):
        # Update time and pressure and temperature values
        self.time_data.append(self.time_data[-1] + 1)
        if len(self.time_data) >= self.axis_end_time:
            self.axis_start_time += 1
            self.axis_end_time += 1

        # Read new data from ADC
        ADC_data = self.ADC.get_next_data_row()
        self.p0_y_data.append(ADC_data.p0)
        self.p1_y_data.append(ADC_data.p1)
        self.p2_y_data.append(ADC_data.p2)
        self.p3_y_data.append(ADC_data.p3)
        self.p4_y_data.append(ADC_data.p4)
        self.t0_y_data.append(ADC_data.t0)

        # Update plots
        self._update_plot("p0_series", "p0_x_axis", self.p0_y_data)
        self._update_plot("p1_series", "p1_x_axis", self.p1_y_data)
        self._update_plot("p2_series", "p2_x_axis", self.p2_y_data)
        self._update_plot("p3_series", "p3_x_axis", self.p3_y_data)
        self._update_plot("p4_series", "p4_x_axis", self.p4_y_data)
        self._update_plot("t0_series", "t0_x_axis", self.t0_y_data)

    def update(self):
        self._update_video()
        self._update_plots()

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
                        # Recording and Calibration Buttons
                        button_y = viewport_height//2 + viewport_height//4 + 50
                        button_x_start = viewport_width//2 - viewport_width//4 - 100
                        button_width = 150
                        button_height = 35
                        button_x_spacing = 300
                        with dpg.group(horizontal=True):
                            dpg.add_button(label="Start Recording", width=button_width, height=button_height,
                                           pos=[button_x_start + button_x_spacing*0, button_y],
                                           tag=self.recording_button_tag)
                            dpg.add_button(label="Calibrate Sensors", width=button_width, height=button_height,
                                           pos=[button_x_start + button_x_spacing*1, button_y],
                                           tag=self.calibrate_button_tag)

                # Right-hand side group
                with dpg.group(horizontal=False, pos=[viewport_width // 2 + 80, 60]) as right_group:
                    # TODO make this an "add plots" function?
                    # Plots
                    dpg.add_text("Live Data", pos=[viewport_width // 2 + viewport_width // 4 + 20, 30])
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
                        # TODO add tooltips to plots with further explanation of where that pressure is occurring
                        # TODO Add text next to the plots with the current numerical value (and update it continually)
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

        # Indicate that this window has been created
        self.is_created = True
