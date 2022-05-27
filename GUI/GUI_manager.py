import dearpygui.dearpygui as dpg
from GUI.window_interface import IWindow
from GUI import welcome_window
from GUI import live_window

# Global variables (only used for the GUI)
LIVE_WINDOW = None
WELCOME_WINDOW = None
CURRENT_WINDOW = None


def init_GUI():
    global LIVE_WINDOW, WELCOME_WINDOW, CURRENT_WINDOW

    # Initialization for DPG
    dpg.create_context()
    dpg.create_viewport(title='Custom Title', width=1920, height=1080)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.maximize_viewport()

    # Get viewport width and height
    viewport_width = dpg.get_viewport_client_width()
    viewport_height = dpg.get_viewport_client_height()

    # Instantiate window classes
    LIVE_WINDOW = live_window.LiveWindow()
    WELCOME_WINDOW = welcome_window.WelcomeWindow()

    # Create windows
    LIVE_WINDOW.create(viewport_width, viewport_height)
    WELCOME_WINDOW.create(viewport_width, viewport_height)

    # Set primary window
    dpg.set_primary_window(WELCOME_WINDOW.tag(), True)
    CURRENT_WINDOW = WELCOME_WINDOW


def run_GUI():
    # Start DPG
    # dpg.start_dearpygui()

    # Render Loop
    # (This replaces start_dearpygui() and runs every frame)
    while dpg.is_dearpygui_running():
        # Update
        # update_video(capture)
        # update_plots()

        # You can manually stop by using stop_dearpygui()
        dpg.render_dearpygui_frame()


def teardown_GUI():
    # Stop DPG
    dpg.destroy_context()


def change_window(to_window: IWindow):
    """
    Used to change from one window to another (shows new window, sets it as primary, and hides the old)
    :param to_window: window object to set as the new primary and visible window
    :return: None
    """
    global CURRENT_WINDOW
    # Show new window
    to_window.show()
    # Set it as the new main window
    to_window.set_primary()
    # Hide the old window
    CURRENT_WINDOW.hide()
    # Update current window global
    CURRENT_WINDOW = to_window


