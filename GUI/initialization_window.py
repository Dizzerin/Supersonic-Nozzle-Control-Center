import dearpygui.dearpygui as dpg
from Interfaces.window_interface import IWindow
from GUI import GUI_manager
from Interfaces.camera_data_provider_interface import ICameraDataProvider
from Interfaces.ADC_data_provider_interface import IADCDataProvider


class InitializationWindow(IWindow):
    def __init__(self, camera_data_provider: ICameraDataProvider, ADC_data_provider: IADCDataProvider):
        # Call super class's init
        super(InitializationWindow, self).__init__()

        # Local vars
        self.ADC_provider = ADC_data_provider
        self.camera_provider = camera_data_provider
        self.camera_index = None
        self.is_created = False
        self.tag = "Init Window"
        self.ADC_ready = False
        self.camera_ready = False
        self.try_initialization = True

    def is_created(self) -> bool:
        return self.is_created

    def tag(self) -> str:
        return self.tag

    def update(self):
        # Only try setup steps on first call or once there has been a new selection
        if self.try_initialization:
            self.try_initialization = False
            # Try to find and initialize ADC
            self.ADC_provider.initialize()
            if not self.ADC_provider.is_ready:
                # Todo display error and don't continue
                pass
            else:
                self.ADC_ready = True

            # Get list of available cameras
            self.camera_provider.get_available_cameras()
            # TODO
            # If none, throw error
            # If multiple:
                # Set default to camera specified in settings/config file
                # Display combo box for user to select which one
            self.camera_index = 0

            # Try to initialize camera
            self.camera_provider.initialize_capture(camera_index=self.camera_index)
            if not self.camera_provider.is_ready:
                # Todo display error and don't continue
                pass
            else:
                self.camera_ready = True

            # # Update progress bar
            # count = dpg.get_value("Progress")
            # count += 0.01
            # dpg.set_value("Progress", count)
            #
            # # Once progress is 100%, go to live window
            # if count == 100:
            #     GUI_manager.change_window(GUI_manager.LIVE_WINDOW)

            if self.ADC_ready and self.camera_ready:
                # GUI_manager.change_window(GUI_manager.LIVE_WINDOW)
                pass

    def create(self, viewport_width: int, viewport_height: int):
        # Local vars
        title_y_start = 80

        # Build the window
        with dpg.window(tag=self.tag, show=True):
            # Add title/subtitle text
            dpg.add_text("Supersonic Nozzle Control Center 0.1.0", pos=[int(viewport_width / 2 - 150), title_y_start])
            dpg.add_text("Initializing...", pos=[int(viewport_width / 2 - 50), title_y_start + 30])

            dpg.add_progress_bar(tag="Progress", overlay="Status")

            # TODO allow these elements to be dynamically added or unhidden
            # Note that the combo box needs to have a callback with sets try initialization to true whenever its selection is changed
            dpg.add_combo(["Camera 1", "Camera 2"], label="Select which camera to use")
            dpg.add_text("Warning, ADC could not be found/initialized!  Cannot continue!")
