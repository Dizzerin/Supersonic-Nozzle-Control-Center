import dearpygui.dearpygui as dpg
from Testing import cv2_testing
import labjacktesting

# TODO TEMP
# Global pressures and other plot data
time_data = [0]
axis_start_time = 0
axis_end_time = 200
num_pressure_plots = 5
plot_height = 150       # pixels
plot_width = 800        # pixels
p0_y_data = []
p1_y_data = []
p2_y_data = []
p3_y_data = []
p4_y_data = []
t0_y_data = []


def update_video(capture):
    raw_data = cv2_testing.get_frame(capture)
    dpg.set_value("texture_tag", raw_data)


def update_plot(series_tag, x_axis_tag, y_data):
    # "Scroll" x-axis
    dpg.set_axis_limits(x_axis_tag, axis_start_time, axis_end_time)

    # Update axis data
    dpg.set_value(series_tag, [time_data, y_data])


def update_plots():
    # TODO don't use global data
    global axis_end_time, axis_start_time, p0_y_data, p1_y_data, p2_y_data, p3_y_data, p4_y_data, t0_y_data, time_data

    # Update time and pressure and temperature values
    time_data.append(time_data[-1] + 1)
    if len(time_data) >= axis_end_time:
        axis_start_time += 1
        axis_end_time += 1

    # Read new data from ADC
    labjack_data = labjacktesting.read_ADC()
    p0_y_data.append(labjack_data.p0)
    p1_y_data.append(labjack_data.p1)
    p2_y_data.append(labjack_data.p2)
    p3_y_data.append(labjack_data.p3)
    p4_y_data.append(labjack_data.p4)
    t0_y_data.append(labjack_data.t0)

    # Update plots
    update_plot("p0_series", "p0_x_axis", p0_y_data)
    update_plot("p1_series", "p1_x_axis", p1_y_data)
    update_plot("p2_series", "p2_x_axis", p2_y_data)
    update_plot("p3_series", "p3_x_axis", p3_y_data)
    update_plot("p4_series", "p4_x_axis", p4_y_data)
    update_plot("t0_series", "t0_x_axis", t0_y_data)


def run_gui(capture):
    # TODO don't use global data
    global axis_end_time, axis_start_time, p0_y_data, p1_y_data, p2_y_data, p3_y_data, p4_y_data, t0_y_data, time_data

    dpg.create_context()
    dpg.create_viewport(title="Supersonic Nozzle Lab")
    dpg.set_viewport_vsync(True)

    raw_data = cv2_testing.get_frame(capture)

    with dpg.texture_registry(show=False):
        dpg.add_raw_texture(640, 480, raw_data, format=dpg.mvFormat_Float_rgba, tag="texture_tag")

    with dpg.window(label="Main Window") as main_window:

        # Master group to divide window into two columns
        with dpg.group(horizontal=True) as master_group:

            # Left-hand side group
            with dpg.group(horizontal=False) as left_group:
                # Video feed
                dpg.add_image("texture_tag")

                # Autofocus checkbox
                with dpg.group(horizontal=True):
                    dpg.add_checkbox(label="Auto Focus", default_value=True, user_data=capture,
                                     callback=cv2_testing.callback_autofocus, tag="auto_focus")
                    # dpg.add_checkbox(label="Auto Exposure")

                # Focus and brightness sliders
                with dpg.group(horizontal=False):
                    # Todo Verify range
                    dpg.add_slider_int(label="Focus", tag="focus", vertical=False, default_value=0, min_value=0,
                                       max_value=1012,
                                       clamped=True, width=100, user_data=capture, callback=cv2_testing.update_focus)
                    # dpg.add_spacer(width=100)
                    dpg.add_slider_int(label="Brightness", tag="brightness", vertical=False, default_value=0,
                                       min_value=-64,
                                       max_value=64, width=100, clamped=True, user_data=capture,
                                       callback=cv2_testing.update_brightness)
                    dpg.add_button(label="Reset brightness", user_data=capture, callback=cv2_testing.brightness_reset_callback)

            # Right-hand side group
            with dpg.group(horizontal=False) as right_group:
                # TODO make this an "add plots" function?
                # Plots
                with dpg.subplots(rows=num_pressure_plots+1, columns=1, row_ratios=[1, 1, 1, 1, 1, 1.3], label="Live Data", width=plot_width,
                                  height=((num_pressure_plots+1)*plot_height+10)) as plot_group:
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
                    # Create pressure plots
                    for i in range(num_pressure_plots):
                        # Add plot
                        with dpg.plot(label="p{}_plot".format(str(i)), no_title=True, no_menus=True):
                            # Create legend
                            dpg.add_plot_legend()
                            # Create x and y axes
                            dpg.add_plot_axis(dpg.mvXAxis, label="", tag="p{}_x_axis".format(str(i)),
                                              no_tick_labels=True)
                            with dpg.plot_axis(dpg.mvYAxis, label="(psi)", tag="p{}_y_axis".format(str(i))):
                                # Create line_series plots
                                dpg.add_line_series(time_data, [], label="Pressure {}".format(str(i)),
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
                            dpg.add_line_series(time_data, [], label="Temperature 0", tag="t0_series")

                # Make "Live Data" label/title of the plot group look nicer
                #   Set PlotPadding to 7 and LabelPadding to 11
                # TODO figure out why this theme isn't applying to the plot_group
                #   Or maybe just add a text label and set its properties instead of adjusting all plots in the group
                with dpg.theme() as plot_group_container_theme:
                    with dpg.theme_component():
                        dpg.add_theme_style(dpg.mvPlotStyleVar_PlotPadding, 10)
                        dpg.add_theme_style(dpg.mvPlotStyleVar_LabelPadding, 10)
                dpg.bind_item_theme(plot_group, plot_group_container_theme)
                # dpg.show_style_editor()

    # Set main window to fill the entire viewport
    dpg.set_primary_window(main_window, True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.maximize_viewport()

    # Render Loop
    # (This replaces start_dearpygui() and runs every frame)
    while dpg.is_dearpygui_running():
        update_video(capture)
        update_plots()

        # Todo temp testing
        # cv2_testing.print_lots_o_stuff(capture)

        # You can manually stop by using stop_dearpygui()
        dpg.render_dearpygui_frame()
    dpg.destroy_context()
