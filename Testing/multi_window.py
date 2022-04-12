import dearpygui.dearpygui as dpg


def change_window():
    dpg.add_window(tag="new window")
    dpg.delete_item("Primary Window")
    dpg.set_primary_window("new window", True)


dpg.create_context()

with dpg.window(tag="Primary Window"):
    dpg.add_text("Hello, world")
    dpg.add_button(label="change primary window", callback=change_window)

dpg.create_viewport(title='Custom Title', width=600, height=200)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
