import time

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
        self.available_cameras = []
        self.camera_index = None
        self.is_created = False
        self.tag = "Init Window"
        self.ADC_ready = False
        self.camera_ready = False
        self.try_initialization = True
        self.num_update_calls = 0

        # UI element tags
        self.no_ADC_warning_tag = "ADC_warning"
        self.no_cam_warning_tag = "camera_warning"
        self.multi_cam_avail_tag = "multi_cam_text"
        self.camera_combo_select_tag = "combo"

    def is_created(self) -> bool:
        return self.is_created

    def tag(self) -> str:
        return self.tag

    def update(self):
        """ The first call to this function occurs before the window is even draw and some initialization steps
        here can take a long time (especially if we have to search through a bunch of cameras etc., so the whole
        point of this screen is to display something while those initialization steps are occurring.  Therefor,
        in order to accomplish this, nothing should be done the first time this function is called in order to allow
        the window to be drawn.  Then the long initialization steps should be done the second time this function is
        called, and then nothing there after since this function is called every frame.  The only time the body of this
        should really be performed is on the second call to this function.
        Update: It actually seems to yield a smoother UI experience if the body is run on the third update call.
        # todo and maybe when the user makes a change?  But maybe that should be handled in callbacks instead
        """
        self.num_update_calls += 1

        # Only try setup steps on second (third now) call or once there has been a new selection
        if self.num_update_calls >= 3 and self.try_initialization:
            self.try_initialization = False

            # Try to find and initialize ADC
            self.ADC_provider.initialize()
            if not self.ADC_provider.is_ready:
                # Show no ADC warning text
                dpg.configure_item(self.no_ADC_warning_tag, show=True)
                # TODO add back/home button and exit button and show them in this case
            else:
                self.ADC_ready = True

            # Try to initialize default camera
            # TODO get default camera from config/settings file
            self.camera_index = 0
            self.camera_provider.initialize_capture(camera_index=self.camera_index)
            if self.camera_provider.is_ready:
                self.camera_ready = True
            # Else find available cameras and get user selection
            else:
                # Get list of available cameras
                # TODO implement multi-threading so this doesn't lock up the UI while it searches for cameras...
                self.available_cameras = self.camera_provider.get_available_cameras()
                # Add available cameras to dropdown selection list
                dpg.configure_item(self.camera_combo_select_tag, items=self.available_cameras)

                # If no available cameras:
                if len(self.available_cameras) == 0:
                    # Show no camera warning text
                    dpg.configure_item(self.no_cam_warning_tag, show=True)
                    # TODO add back/home button and exit button and show them in this case
                elif len(self.available_cameras) == 1:
                    # Use the only available camera (This code will run if only 1 camera is available and it is not the default one in the settings file)
                    self.camera_index = self.available_cameras[0]
                    # Initialize capture with that camera
                    self.camera_provider.initialize_capture(camera_index=self.camera_index)
                    if self.camera_provider.is_ready:
                        self.camera_ready = True
                else:
                    # Display info text about multiple cameras being available
                    dpg.configure_item(self.multi_cam_avail_tag, show=True)

                    # Display combo box for user to select camera
                    dpg.configure_item(self.camera_combo_select_tag, show=True)
                    # TODO actually get camera index from user selection or file or default etc. -- will need callback

        # Once everything is ready, proceed to live session window
        if self.ADC_ready and self.camera_ready:
            # TODO this doesn't work, fix this bug!
            # GUI_manager.change_window(GUI_manager.LIVE_WINDOW)
            pass

    def create(self, viewport_width: int, viewport_height: int):
        # Include title bar on this screen
        GUI_manager.enable_title_bar()

        # Local vars
        title_y_start = 80

        # Build the window
        with dpg.window(tag=self.tag, show=True):
            # TODO Verify positioning of all objects on this window

            dpg.add_button(label="Home", callback=lambda: GUI_manager.change_window(GUI_manager.WELCOME_WINDOW))

            # Add title/subtitle text
            dpg.add_text("Supersonic Nozzle Control Center 0.1.0", pos=[int(viewport_width / 2 - 130), title_y_start])
            dpg.add_text("Initializing...", pos=[int(viewport_width / 2 - 50), title_y_start + 30])
            dpg.add_loading_indicator(pos=[int(viewport_width / 2 - 20), title_y_start + 70])

            # ADC warning (hidden by default)
            dpg.add_text("Warning, ADC unit could not be found/initialized!  Cannot continue!",
                         tag=self.no_ADC_warning_tag, pos=[int(viewport_width / 2 - 100), title_y_start + 90], show=False)

            # Camera warning (hidden by default)
            dpg.add_text("Warning, No cameras could be found/initialized!  Cannot continue!",
                         tag=self.no_cam_warning_tag, pos=[int(viewport_width / 2 - 100), title_y_start + 90], show=False)

            # Text asking user to select which camera to use when multiple cameras are available (hidden by default)
            dpg.add_text("Multiple cameras are available, Please select which one you would like to use.",
                         tag=self.multi_cam_avail_tag, pos=[int(viewport_width / 2 - 100), title_y_start + 90], show=False)

            # Combo box to allow user to select which camera to use
            # Note that the combo box needs to have a callback with sets try initialization to true whenever its selection is changed
            dpg.add_combo(["Camera " + str(x + 1) for x in self.available_cameras], tag=self.camera_combo_select_tag,
                          label="Select which camera to use", width=200, pos=[int(viewport_width / 2 - 80), title_y_start + 120], show=False)

        # Indicate that this window has been created
        self.is_created = True
