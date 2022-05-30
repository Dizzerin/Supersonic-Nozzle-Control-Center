from Interfaces.camera_data_provider_interface import ICameraDataProvider
import dearpygui.dearpygui as dpg
from typing import List
"""
This is a test data provider which implements the camera data provider interface (ICameraDataProvider)
This device can be supplied to the main application instead of the PCBCamera device or any other device
It simply returns a static image

This class is used for testing purposes
"""
# TODO actually write/complete this test class
# TODO make it do the above, perhaps later also return video?


class TestCamera(ICameraDataProvider):
    def __init__(self, width, height):
        # Call super class's init
        super(TestCamera, self).__init__(width, height)

        # Local vars
        self.is_ready = False
        self.AF_enabled = True
        self.camera_index = None
        self.width = width
        self.height = height

        # Initialize PCB Camera Capture
        self.capture = None

    def get_available_cameras(self) -> List[int]:
        # Return random list of cameras indexes available
        return [0, 2, 3]
