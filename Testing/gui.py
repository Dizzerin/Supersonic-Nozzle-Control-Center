import dearpygui.dearpygui as dpg
from Testing import cv2_testing
import random
import labjacktesting

# TODO TEMP
time_data = [0]
axis_start_time = 0
axis_end_time = 200
pressure_1_y_data = []
pressure_2_y_data = []


def update_plot(series_tag, x_axis_tag, y_data):
    # "Scroll" x-axis
    dpg.set_axis_limits(x_axis_tag, axis_start_time, axis_end_time)

    # Update axis data
    dpg.set_value(series_tag, [time_data, y_data])


def run_gui(capture):
    # TODO don't use global data
    global axis_end_time, axis_start_time, pressure_1_y_data, time_data

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

                # Autofocus checkbox and reset button
                with dpg.group(horizontal=True):
                    dpg.add_checkbox(label="Auto Focus", default_value=True, user_data=capture,
                                     callback=cv2_testing.callback_autofocus, tag="auto_focus")
                    # Todo below doesn't actually update brightness, just the slider
                    dpg.add_button(label="reset", callback=lambda sender, data: dpg.set_value("brightness", value=0))
                    # dpg.add_checkbox(label="Auto Exposure")

                # Focus and brightness sliders
                with dpg.group(horizontal=False):
                    # Todo Verify range
                    dpg.add_slider_int(label="Focus", tag="focus", vertical=False, default_value=0, min_value=0, max_value=1012,
                                       clamped=True, width=100, user_data=capture, callback=cv2_testing.update_focus)
                    # dpg.add_spacer(width=100)
                    dpg.add_slider_int(label="Brightness", tag="brightness", vertical=False, default_value=0, min_value=-64,
                                       max_value=64, width=100, clamped=True, user_data=capture,
                                       callback=cv2_testing.update_brightness)
            # Right-hand side group
            with dpg.group(horizontal=False) as right_group:

                # Plots
                with dpg.group() as plot_group:

                    # Pressure 1 Plot
                    with dpg.plot(label="Live Pressure Data", tag="p1_plot", height=200, width=800):
                        # Create legend
                        dpg.add_plot_legend()

                        # Create x and y axes
                        dpg.add_plot_axis(dpg.mvXAxis, label="time (s)", tag="p1_x_axis")
                        dpg.add_plot_axis(dpg.mvYAxis, label="pressure (psi)", tag="p1_y_axis")
                        dpg.set_axis_limits_auto("p1_y_axis")

                        # Create line_series plots
                        dpg.add_line_series(time_data, pressure_1_y_data, label="Pressure 1", parent="p1_y_axis", tag="p1_series")

                    # Pressure 2 Plot
                    with dpg.plot(label="p1_plot", tag="p2_plot", height=200, width=800):
                        # Create legend
                        dpg.add_plot_legend()

                        # Create x and y axes
                        dpg.add_plot_axis(dpg.mvXAxis, label="time (s)", tag="p2_x_axis")
                        dpg.add_plot_axis(dpg.mvYAxis, label="pressure (psi)", tag="p2_y_axis")
                        dpg.set_axis_limits_auto("p2_y_axis")

                        # Create line_series plots
                        dpg.add_line_series(time_data, pressure_2_y_data, label="Pressure 2", parent="p2_y_axis", tag="p2_series")


    # Set main window to fill the entire viewport
    dpg.set_primary_window(main_window, True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.maximize_viewport()

    # Render Loop:
    # (This replaces start_dearpygui() and runs every frame)
    while dpg.is_dearpygui_running():
        raw_data = cv2_testing.get_frame(capture)
        dpg.set_value("texture_tag", raw_data)

        # Todo temp testing
        # cv2_testing.print_lots_o_stuff(capture)
        # labjacktesting.testU12()

        # Update time and pressure and temperature values
        time_data.append(time_data[-1] + 1)
        if len(time_data) >= axis_end_time:
            axis_start_time += 1
            axis_end_time += 1

        labjack_data = labjacktesting.read_ADC()
        pressure_1_y_data.append(labjack_data.p1)
        pressure_2_y_data.append(labjack_data.p2)

        # Update plots
        update_plot("p1_series", "p1_x_axis", pressure_1_y_data)
        update_plot("p2_series", "p2_x_axis", pressure_2_y_data)

        # You can manually stop by using stop_dearpygui()
        dpg.render_dearpygui_frame()
    dpg.destroy_context()
