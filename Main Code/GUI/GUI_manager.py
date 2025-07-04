import os
import sys
import traceback
from datetime import datetime
import logging
from queue import Queue
from threading import Thread

import dearpygui.dearpygui as dpg

from Custom_Types.custom_types import DataStore
from Software_Interfaces.window_interface import IWindow
from Hardware_Interfaces.camera_data_provider_interface import ICameraDataProvider
from Hardware_Interfaces.ADC_data_provider_interface import IADCDataProvider
from Hardware_Interfaces.ADC_data_writer_interface import IADCDataWriter
from Software_Interfaces.config_handler_interface import IConfigHandler
from GUI import initialization_window, welcome_window, live_window, about_window

# Global variables (only used for the GUI)
# TODO (skip) maybe later make these not globals (create these windows in init function, return them, and pass them into the
#   constructor of any other windows that need to use these (i.e. next_window)
#   this would also make it so the create functions wouldn't be needed and could be done inside the concrete class's init
INITIALIZATION_WINDOW = None
LIVE_WINDOW = None
WELCOME_WINDOW = None
CURRENT_WINDOW = None
ABOUT_WINDOW = None
# Global variable to store the last exception
last_exception = None

# Get viewport width and height
# viewport_width = dpg.get_viewport_client_width()    # 1904
# viewport_height = dpg.get_viewport_client_height()  # 1041
viewport_width = 1920
viewport_height = 1080

# TODO (skip) Make this log file location and name configurable
log_file = "Supersonic Nozzle Control Center Error Log.txt"

logging.basicConfig(
    filename=log_file,
    level=logging.ERROR,
    format='%(message)s',
    filemode='a'  # Append to the file
)


def display_pre_init_error_GUI(exception: Exception):
    # Initialization for DPG
    dpg.create_context()
    dpg.create_viewport(title="Supersonic Nozzle Control Center", width=1920, height=1080, resizable=False)

    dpg.set_viewport_vsync(True)  # Match display's refresh rate


    dpg.setup_dearpygui()
    dpg.show_viewport()

    # TODO (skip) see matching code for notes about this
    # dpg.maximize_viewport()
    dpg.set_viewport_width(1936)
    dpg.set_viewport_height(1056)
    # Get viewport width and height
    # viewport_width = dpg.get_viewport_client_width()
    # viewport_height = dpg.get_viewport_client_height()
    global viewport_width
    global viewport_height
    title_bar_height = 71  # Adjustment factor to account for title bar, task bar, and dear py gui/windows 11 bugs -- amount to trim background image by so no scrollbar shows

    # Don't show title bar
    # dpg.set_viewport_decorated(False)

    # Local vars
    # Note: These are only used for the button on this screen
    # Todo (skip) implement some of this as a style and make the text larger and apply the style to these buttons instead
    button_y_start = viewport_height / 2 + 60
    button_width = 150
    button_height = 35
    button_y_spacing = 60  # Number of vertical pixels between top of one button to top of next only for Welcome Window buttons

    # Create textures/images (which will later be added to the window)
    # width1, height1, channels1, data1 = dpg.load_image(r"Image_Resources/Logo2.png")
    # width2, height2, channels2, data2 = dpg.load_image(r"Image_Resources/Red_Room_Red_Text.png")
    # width2, height2, channels2, data2 = dpg.load_image(r"Image_Resources/Red_Room_Blue_Text.png")
    # width2, height2, channels2, data2 = dpg.load_image(r"Image_Resources/Blue_Room_Blue_Text.png")
    # width2, height2, channels2, data2 = dpg.load_image(r"Image_Resources/Blue_Room_Blue_Text_Lots_Of_Roof.png")
    # width2, height2, channels2, data2 = dpg.load_image(r"Image_Resources/Red_Room_Blue_Text_Lots_Of_Roof.png")
    width2, height2, channels2, data2 = dpg.load_image(r"Image_Resources/Red_Room_Red_Text_Lots_Of_Roof.png")
    with dpg.texture_registry():
        # dpg.add_static_texture(width=width1, height=height1, default_value=data1, tag="title_image")
        dpg.add_static_texture(width=width2, height=height2-title_bar_height, default_value=data2, tag="background_image")

    # Build pre-init-error-window
    with dpg.window(tag="pre-init-error-window", show=True, no_scrollbar=True):
        # Add background image
        dpg.add_image("background_image", pos=[0, 0])

        # dpg.add_text("ERROR!\n"
        #              "There has been an error during initialization that\n"
        #              "is preventing the program from continuing!",
        #              pos=[viewport_width//2-150, viewport_height//2],
        #              wrap=viewport_width-200)

        dpg.add_button(label="Exit", width=button_width, height=button_height,
                       pos=[int(viewport_width / 2 - button_width / 2), button_y_start + 3 * button_y_spacing],
                       callback=dpg.stop_dearpygui)

    global last_exception
    last_exception = sys.exc_info()  # Store the exception
    _show_error_window_and_log_exception(exception)

    dpg.start_dearpygui()


def init_GUI(camera_data_provider: ICameraDataProvider, ADC_data_provider: IADCDataProvider,
             ADC_data_writer: IADCDataWriter, config_handler: IConfigHandler, data_store: DataStore, sample_thread: Thread):
    global INITIALIZATION_WINDOW, LIVE_WINDOW, WELCOME_WINDOW, CURRENT_WINDOW, ABOUT_WINDOW

    # Initialization for DPG
    dpg.create_context()
    dpg.create_viewport(title="Supersonic Nozzle Control Center", width=1920, height=1080, resizable=False)
    dpg.set_viewport_pos([0, 0])  # Ensure its in the top left of the screen
    dpg.set_viewport_vsync(True)  # Match display's refresh rate

    # Construct the path to the icon file relative to the script directory
    icon_path = os.path.abspath(os.path.join('Image_Resources', 'super_sonic_icon.ico'))
    # Set the icon
    if os.path.exists(icon_path):
        dpg.set_viewport_small_icon(icon_path)
        dpg.set_viewport_large_icon(icon_path)
    else:
        print(f"Icon file not found at: {icon_path}")

    dpg.setup_dearpygui()
    dpg.show_viewport()

    # TODO Note: (skip) update the display size stuff later and fix it if DPG/windows bugs are ever fixed
    #   There is a bug (or several) in DearPyGUI that prevent windows from being sized properly...
    #   If I try to fix it to 1920x1080 it sets it to 1904x1041
    #   If I hide the title bar the alignment of the button click boxes gets messed up
    #   etc. etc.  These may be Windows 10-11 specific issues, I'm not sure.
    #   But ultimately, I want this to work on Windows on the lab computer that its designed for and I want it to not show up really badly and weirdly on monitors that are higher resolution should the lab ever get a monitor with higher resolution.
    #   The sizing is currently all hardcoded for 1920x1080, I originally designed it to be full screened, but in order to make it more compatible
    #   across more monitor sizes I'm no longer calling maximize_viewport() and I also decided to add the title bar back in for ease of use
    #   On the lab computer, with the title bar and the DearPyGUI/Windows issues and the Windows taskbar showing, in order to get a full screen viewport, I have to set the viewport to
    #   1936x1056, so that's what I'm doing.  Since I based all my positioning calculations off other values though, I'm manually passing into the window creation functions the actual resolution that should be used that it was designed for
    # dpg.maximize_viewport()
    dpg.set_viewport_width(1936)
    dpg.set_viewport_height(1056)
    # Get viewport width and height
    # viewport_width = dpg.get_viewport_client_width()
    # viewport_height = dpg.get_viewport_client_height()
    global viewport_width
    global viewport_height

    # Instantiate window classes
    INITIALIZATION_WINDOW = initialization_window.InitializationWindow(camera_data_provider, ADC_data_provider, sample_thread)
    LIVE_WINDOW = live_window.LiveWindow(camera_data_provider, ADC_data_provider, ADC_data_writer, data_store)
    WELCOME_WINDOW = welcome_window.WelcomeWindow(config_handler)
    ABOUT_WINDOW = about_window.AboutWindow()

    # Create first window
    WELCOME_WINDOW.create(viewport_width, viewport_height)

    # Set primary window
    WELCOME_WINDOW.set_primary()
    CURRENT_WINDOW = WELCOME_WINDOW


def run_GUI(sample_thread_error_queue: Queue):
    # Render Loop
    # (This replaces start_dearpygui() and runs every frame)
    while dpg.is_dearpygui_running():
        # Render next frame
        dpg.render_dearpygui_frame()

        # Save present window
        present_window = CURRENT_WINDOW

        global last_exception

        # Call the present window's update function
        try:
            present_window.update()  # Note: this function could change the current window global

            # Also check sampling thread and see if it has had any errors
            if not sample_thread_error_queue.empty():
                error = sample_thread_error_queue.get(block=False)
                sample_thread_error_queue.task_done()
                print(f"Fatal error occurred in sampling thread! Error info: {error}")
                # Throw error in this main thread that was raised in the sampling thread
                raise error

        # Catch all errors, show them before exiting
        except Exception as ex:
            last_exception = sys.exc_info()  # Store the exception
            change_window(WELCOME_WINDOW)
            _show_error_window_and_log_exception(ex)

        # When switching windows call the new window's update function
        if CURRENT_WINDOW is not present_window:
            CURRENT_WINDOW.update()


def teardown_GUI():
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
        # viewport_width = dpg.get_viewport_client_width()
        # viewport_height = dpg.get_viewport_client_height()
        global viewport_width
        global viewport_height

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


def _show_error_window_and_log_exception(exception: Exception):
    # Log exception/fatal error info
    global last_exception
    if last_exception:
        exc_type, exc_value, exc_traceback = last_exception
        exc_str = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        # Print exception and traceback to console
        print("--------------------------------------")
        print(f"Fatal Error ({datetime.now()})")
        print(exc_str)
        print(exception)
        # Print exception and traceback to log file
        logging.error("--------------------------------------")
        logging.error(f"Fatal Error ({datetime.now()})")
        logging.error(exc_str)
        logging.error(exception)

    # Determine viewport size
    # viewport_width = dpg.get_viewport_client_width()
    # viewport_height = dpg.get_viewport_client_height()
    global viewport_width
    global viewport_height

    # Window size (Note: This isn't fully used)
    window_width = 300
    window_height = 100

    # Calculate center position
    x_position = (viewport_width - window_width) // 2
    y_position = (viewport_height - window_height) // 2

    def _on_exit(sender, app_data, user_data):
        # Get rid of confirmation window
        dpg.delete_item("Error Window")

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
            no_collapse=True,
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
