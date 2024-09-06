import dearpygui.dearpygui as dpg


def report_viewport_size():
    # Get the current width and height of the viewport
    viewport_width = dpg.get_viewport_width()
    viewport_height = dpg.get_viewport_height()
    # Print or display the dimensions
    print(f"Viewport Width: {viewport_width}, Height: {viewport_height}")

def main():
    dpg.create_context()

    viewport_width = 1920
    viewport_height = 1080

    dpg.create_viewport(title='DearPyGui Window', width=viewport_width, height=viewport_height, resizable=False)

    with dpg.window(tag="main", label="Fixed Size Window", width=viewport_width, height=viewport_height, no_resize=True):
        dpg.add_text("This should be 1920x1080, but its not... at least not on windows 11.")
        # Add a button that reports the viewport size
        dpg.add_button(label="Report Viewport Size", callback=report_viewport_size) # -- reports 1936x1056 on Windows 11 when maximized on a 1920x1080 screen with the taskbar on the windows system shown and the window title bar shown

    dpg.set_primary_window("main", True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()