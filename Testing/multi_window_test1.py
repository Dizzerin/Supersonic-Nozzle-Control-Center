import dearpygui.dearpygui as dpg
"""
This tests switching between two windows by recreating them each time
setting the new one as the primary window, and then deleting the old window
"""


def change_window(creation_function, from_label, to_label):
    # dpg.add_window(tag="new window")
    # Create new window
    creation_function()
    # Set it as the new main window
    dpg.set_primary_window(to_label, True)
    # Delete the old window
    dpg.delete_item(from_label)


def create_first_window():
    with dpg.window(tag="first window"):
        dpg.add_text("This is the first window")
        dpg.add_button(label="change primary window", callback=lambda: change_window(create_second_window, "first window", "second window"))


def create_second_window():
    with dpg.window(tag="second window"):
        dpg.add_text("This is the second window")
        dpg.add_button(label="change primary window", callback=lambda: change_window(create_first_window, "second window", "first window"))


dpg.create_context()
create_first_window()

dpg.create_viewport(title='Custom Title', width=600, height=200)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("first window", True)
dpg.start_dearpygui()
dpg.destroy_context()
