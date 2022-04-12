import array
import dearpygui.dearpygui as dpg

# Temp Global
raw_data = []


def update_dynamic_texture(sender, app_data, user_data):
    new_color = dpg.get_value(sender)
    new_color[0] = new_color[0] / 255
    new_color[1] = new_color[1] / 255
    new_color[2] = new_color[2] / 255
    new_color[3] = new_color[3] / 255

    global raw_data
    for j in range(0, 480 * 640 * 4):
        raw_data[j] = new_color[j % 4]


def run_gui():
    dpg.create_context()
    dpg.create_viewport(title="Supersonic Nozzle Lab")

    texture_data = []
    for i in range(0, 480 * 640):
        texture_data.append(255 / 255)
        texture_data.append(0)
        texture_data.append(255 / 255)
        texture_data.append(255 / 255)

    global raw_data
    raw_data = array.array('f', texture_data)

    with dpg.texture_registry(show=False):
        # dpg.add_dynamic_texture(100, 100, texture_data, tag="texture_tag")
        dpg.add_raw_texture(640, 480, raw_data, format=dpg.mvFormat_Float_rgba, tag="texture_tag")

    with dpg.window(label="Main Window") as main_window:
        dpg.add_image("texture_tag")

        dpg.add_color_picker((255, 0, 255, 255), label="Texture",
                             no_side_preview=True, alpha_bar=True, width=200,
                             callback=update_dynamic_texture)

    # Set main window to fill the entire viewport
    dpg.set_primary_window(main_window, True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.maximize_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


