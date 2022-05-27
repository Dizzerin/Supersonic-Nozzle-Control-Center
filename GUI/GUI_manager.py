import dearpygui.dearpygui as dpg
from Interfaces.window_interface import IWindow
from Interfaces.camera_data_provider_interface import ICameraDataProvider
from Interfaces.ADC_data_provider_interface import IADCDataProvider
from GUI import welcome_window
from GUI import live_window
from GUI import initialization_window

# Global variables (only used for the GUI)
INITIALIZATION_WINDOW = None
LIVE_WINDOW = None
WELCOME_WINDOW = None
CURRENT_WINDOW = None


def init_GUI(camera_data_provider: ICameraDataProvider, ADC_data_provider: IADCDataProvider):
    global INITIALIZATION_WINDOW, LIVE_WINDOW, WELCOME_WINDOW, CURRENT_WINDOW

    # Initialization for DPG
    dpg.create_context()
    dpg.create_viewport(title='Custom Title', width=1920, height=1080)
    dpg.set_viewport_vsync(True)  # TODO do we want this?
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.maximize_viewport()

    # Get viewport width and height
    viewport_width = dpg.get_viewport_client_width()
    viewport_height = dpg.get_viewport_client_height()

    # Instantiate window classes
    INITIALIZATION_WINDOW = initialization_window.InitializationWindow(camera_data_provider, ADC_data_provider)
    LIVE_WINDOW = live_window.LiveWindow(camera_data_provider, ADC_data_provider)
    WELCOME_WINDOW = welcome_window.WelcomeWindow()

    # Create first window
    WELCOME_WINDOW.create(viewport_width, viewport_height)

    # Set primary window
    dpg.set_primary_window(WELCOME_WINDOW.tag, True)
    CURRENT_WINDOW = WELCOME_WINDOW


def run_GUI():
    # Start DPG
    # dpg.start_dearpygui()

    # Render Loop
    # (This replaces start_dearpygui() and runs every frame)
    while dpg.is_dearpygui_running():
        # Call the current window's update function
        CURRENT_WINDOW.update()

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
    # If the to_window hasn't been created yet, create it
    if not to_window.is_created:
        # Get viewport width and height
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()
        # Create the window
        to_window.create(viewport_width, viewport_height)

    # Show new window
    to_window.show()
    # Set it as the new main window
    to_window.set_primary()
    # Hide the old window
    CURRENT_WINDOW.hide()
    # Update current window global
    CURRENT_WINDOW = to_window


