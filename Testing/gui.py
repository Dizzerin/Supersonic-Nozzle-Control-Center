import dearpygui.dearpygui as dpg
from Testing import cv2_testing
import random
import labjacktesting

# TODO TEMP
xdata = list(range(0, 10))


def update_series(sender, data):
    # update x data
    xdata.pop(0)
    xdata.append(xdata[len(xdata) - 1] + 1)
    dpg.set_value('series_tag', [xdata, random.sample(range(0, 10), 10)])
    dpg.set_item_label('series_tag', "new data")
    dpg.set_axis_limits("x_axis", min(xdata), max(xdata))


def run_gui(capture):
    dpg.create_context()
    dpg.create_viewport(title="Supersonic Nozzle Lab")
    dpg.set_viewport_vsync(True)

    raw_data = cv2_testing.get_frame(capture)

    with dpg.texture_registry(show=False):
        dpg.add_raw_texture(640, 480, raw_data, format=dpg.mvFormat_Float_rgba, tag="texture_tag")

    with dpg.window(label="Main Window") as main_window:
        dpg.add_image("texture_tag")

        with dpg.group(horizontal=True):
            dpg.add_checkbox(label="Auto Focus", default_value=True, user_data=capture,
                             callback=cv2_testing.callback_autofocus, tag="auto_focus")
            # Todo below doesn't actually update brightness, just the slider
            dpg.add_button(label="reset", callback=lambda sender, data: dpg.set_value("brightness", value=0))
            # dpg.add_checkbox(label="Auto Exposure")

        with dpg.group(horizontal=True):
            # Todo Verify range
            dpg.add_slider_int(label="Focus", tag="focus", vertical=True, default_value=0, min_value=0, max_value=1012,
                               clamped=True, user_data=capture, callback=cv2_testing.update_focus)
            # dpg.add_spacer(width=100)
            dpg.add_slider_int(label="Brightness", tag="brightness", vertical=True, default_value=0, min_value=-64,
                               max_value=64,
                               clamped=True, user_data=capture, callback=cv2_testing.update_brightness)

        with dpg.group():
            dpg.add_button(label="Update Series", callback=update_series)
            # create plot
            with dpg.plot(label="Line Series", height=400, width=400):
                # create legend
                dpg.add_plot_legend()

                # REQUIRED: create x and y axes
                dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="x_axis")
                dpg.set_axis_limits_auto("x_axis")
                dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")

                # series belong to a y axis
                dpg.add_line_series(list(range(5, 15)), random.sample(range(0, 10), 10), label="original data",
                                    parent="y_axis",
                                    tag="series_tag")

    # Set main window to fill the entire viewport
    dpg.set_primary_window(main_window, True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.maximize_viewport()

    def changeTheWindow(c: IWindow, new: IWindow):
        new.show()
        c.remove()
        dpg.set_primary_window(new.name(), True)

    window = MainWindow()

    # below replaces, start_dearpygui()
    while dpg.is_dearpygui_running():
        # insert here any code you would like to run in the render loop
        raw_data = cv2_testing.get_frame(capture)
        dpg.set_value("texture_tag", raw_data)

        # Todo temp testing
        # cv2_testing.print_lots_o_stuff(capture)
        labjacktesting.testU12()

        new_window = window.update()
        if new_window is not None:
            change_window(window, new_window)
            window = new_window

        # you can manually stop by using stop_dearpygui()
        dpg.render_dearpygui_frame()
    dpg.destroy_context()
