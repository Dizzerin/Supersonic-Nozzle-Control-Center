import sys
import traceback
from datetime import datetime
import logging

import dearpygui.dearpygui as dpg
from Software_Interfaces.window_interface import IWindow
from Hardware_Interfaces.camera_data_provider_interface import ICameraDataProvider
from Hardware_Interfaces.ADC_data_provider_interface import IADCDataProvider
from Hardware_Interfaces.ADC_data_writer_interface import IADCDataWriter
from Software_Interfaces.config_handler_interface import IConfigHandler
from GUI import initialization_window, welcome_window, live_window, about_window

# Global variables (only used for the GUI)
# TODO (optional) maybe later make these not globals (create these windows in init function, return them, and pass them into the
#   constructor of any other windows that need to use these (i.e. next_window)
#   this would also make it so the create functions wouldn't be needed and could be done inside the concrete class's init
INITIALIZATION_WINDOW = None
LIVE_WINDOW = None
WELCOME_WINDOW = None
CURRENT_WINDOW = None
ABOUT_WINDOW = None
# Global variable to store the last exception
last_exception = None

# TODO (optional) Make this log file location and name configurable
log_file = "Supersonic Nozzle Control Center Error Log.txt"

logging.basicConfig(
    filename=log_file,
    level=logging.ERROR,
    format='%(message)s',
    filemode='a'  # Append to the file
)

def init_GUI(camera_data_provider: ICameraDataProvider, ADC_data_provider: IADCDataProvider,
             ADC_data_writer: IADCDataWriter, config_handler: IConfigHandler):
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
    LIVE_WINDOW = live_window.LiveWindow(camera_data_provider, ADC_data_provider, ADC_data_writer)
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
        try:
            present_window.update()  # Note: this function could change the current window global
        # Catch all errors, show them before exiting
        except Exception as ex:
            global last_exception
            last_exception = sys.exc_info()  # Store the exception
            change_window(WELCOME_WINDOW)
            _show_error_window(ex)

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


def _show_error_window(exception: Exception):
    # Determine viewport size
    viewport_width = dpg.get_viewport_client_width()
    viewport_height = dpg.get_viewport_client_height()

    # Window size (Note: This isn't fully used)
    window_width = 300
    window_height = 100

    # Calculate center position
    x_position = (viewport_width - window_width) // 2
    y_position = (viewport_height - window_height) // 2

    def _on_exit(sender, app_data, user_data):
        # Get rid of confirmation window
        dpg.delete_item("Error Window")

        # Log exception/fatal error info
        global last_exception
        if last_exception:
            exc_type, exc_value, exc_traceback = last_exception
            exc_str = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            # Print exception and traceback to console
            print("--------------------------------------")
            print(f"Fatal Error ({datetime.now()})")
            print(exc_str)
            print("--------------------------------------")
            # Print exception and traceback to log file
            logging.error("--------------------------------------")
            logging.error(f"Fatal Error ({datetime.now()})")
            logging.error(exc_str)

        # Exit program
        teardown_GUI()

        # Attempt to re-raise the exception
        # Note: This doesn't actually seem to work, probably because of multi-threading stuff...
        # Note, user_data is the exception - basically same as last_exception
        raise user_data

    with dpg.window(
            label="Error!",
            tag="Error Window",
            no_close=True,
            autosize=True,
            pos=(x_position, y_position)  # Center the window (this won't be exact because of the auto size)
    ):
        dpg.add_text("A fatal error has occurred!")
        dpg.add_text(f"Error Type: {type(exception).__name__}")
        dpg.add_text(f"Exception info: {str(exception)}",
                     wrap=window_width - 20)  # Wrap text with some padding
        dpg.add_text(f"For more information, see log file: \"{log_file}\"",
                     wrap=window_width - 20)  # Wrap text with some padding

        # Exit button
        dpg.add_button(label="Exit", width=75, user_data=exception, callback=_on_exit)
