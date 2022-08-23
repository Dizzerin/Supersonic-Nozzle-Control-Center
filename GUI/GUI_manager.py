import dearpygui.dearpygui as dpg
from Interfaces.window_interface import IWindow
from Interfaces.camera_data_provider_interface import ICameraDataProvider
from Interfaces.ADC_data_provider_interface import IADCDataProvider
from Interfaces.config_handler_interface import IConfigHandler
from GUI import initialization_window, welcome_window, live_window, about_window

# Global variables (only used for the GUI)
# TODO maybe later make these not globals (create these windows in init function, return them, and pass them into the
#   constructor of any other windows that need to use these (i.e. next_window)
#   this would also make it so the create functions wouldn't be needed and could be done inside the concrete class's init
INITIALIZATION_WINDOW = None
LIVE_WINDOW = None
WELCOME_WINDOW = None
CURRENT_WINDOW = None
ABOUT_WINDOW = None


def init_GUI(camera_data_provider: ICameraDataProvider, ADC_data_provider: IADCDataProvider, config_handler: IConfigHandler):
    global INITIALIZATION_WINDOW, LIVE_WINDOW, WELCOME_WINDOW, CURRENT_WINDOW, ABOUT_WINDOW

    # Initialization for DPG
    dpg.create_context()
    dpg.create_viewport(title="Supersonic Nozzle Control Center", width=1920, height=1080)
    dpg.set_viewport_vsync(True)  # Match display's refresh rate
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.maximize_viewport()

    # Get viewport width and height
    viewport_width = dpg.get_viewport_client_width()
    viewport_height = dpg.get_viewport_client_height()

    # Instantiate window classes
    INITIALIZATION_WINDOW = initialization_window.InitializationWindow(camera_data_provider, ADC_data_provider)
    LIVE_WINDOW = live_window.LiveWindow(camera_data_provider, ADC_data_provider)
    WELCOME_WINDOW = welcome_window.WelcomeWindow(config_handler)
    ABOUT_WINDOW = about_window.AboutWindow()

    # Create first window
    WELCOME_WINDOW.create(viewport_width, viewport_height)

    # Set primary window
    WELCOME_WINDOW.set_primary()
    CURRENT_WINDOW = WELCOME_WINDOW


def run_GUI():
    # Render Loop
    # (This replaces start_dearpygui() and runs every frame)
    while dpg.is_dearpygui_running():
        # Render next frame
        dpg.render_dearpygui_frame()

        # Save present window
        present_window = CURRENT_WINDOW

        # Call the present window's update function
        present_window.update()  # Note: this function could change the current window global

        # When switching windows call the new window's update function
        if CURRENT_WINDOW is not present_window:
            CURRENT_WINDOW.update()


def teardown_GUI():
    # TODO save files etc? (decide where to do that and organize it)
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

    # Ensure these all occur in the same frame
    with dpg.mutex():
        # Show new window
        to_window.show()
        # Set it as the new main window
        to_window.set_primary()
        # Hide the old window
        CURRENT_WINDOW.hide()
        # Update current window global
        CURRENT_WINDOW = to_window
