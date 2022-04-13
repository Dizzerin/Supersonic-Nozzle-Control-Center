import dearpygui.dearpygui as dpg
"""
This tests switching between two windows by first creating them both (with one hidden)
and then alternating which one is hidden and which one is show and which one is the primary window
"""


def change_window(from_label, to_label):
    # dpg.add_window(tag="new window")
    # Show new window
    dpg.configure_item(to_label, show=True)
    # Set it as the new main window
    dpg.set_primary_window(to_label, True)
    # Hide the old window
    dpg.configure_item(from_label, show=False)


dpg.create_context()

# Create first window (not hidden)
with dpg.window(tag="first window", show=True):
    dpg.add_text("This is the first window")
    dpg.add_button(label="change primary window", callback=lambda: change_window("first window", "second window"))

# Create second window (hidden)
with dpg.window(tag="second window", show=False):
    dpg.add_text("This is the second window")
    dpg.add_button(label="change primary window", callback=lambda: change_window("second window", "first window"))

dpg.create_viewport(title='Custom Title', width=600, height=200)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("first window", True)
dpg.start_dearpygui()
dpg.destroy_context()
