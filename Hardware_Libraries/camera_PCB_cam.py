from Interfaces.camera_data_provider_interface import ICameraDataProvider
import dearpygui.dearpygui as dpg
from typing import List
import numpy as np
import cv2 as cv
import os


class PCBCamera(ICameraDataProvider):
    def __init__(self):
        # Call super class's init
        super(PCBCamera, self).__init__()

        # Local vars
        self.is_ready = False
        self.AF_enabled = True
        self.camera_index = None

        # Initialize PCB Camera Capture
        self.capture = None

    def get_available_cameras(self) -> List[int]:
        # Iterates through the first 10 indexes
        #   Tries to start a capture with each one, if it works,
        #   it adds that camera index to the list of valid camera indexes.
        #   Note: Sometimes a camera may be at index 0, none on 1, and then another one on 2
        #   i.e. there can be emtpy indexes between valid cameras
        #   This method may seem clunky, but this is the best way right now that is os
        #   independent that I could find online
        # TODO THIS ROUTINE TAKES A LONG TIME =(
        index = 0
        arr = []
        i = 10
        while i > 0:
            cap = cv.VideoCapture(index)
            if cap.read()[0]:
                arr.append(index)
                cap.release()
            index += 1
            i -= 1
        return arr

    def initialize_capture(self, camera_index: int):
        self.camera_index = camera_index

        # Create a capture from camera
        if os.name == 'nt':
            # Use DSHOW only if running on Windows and DSHOW is windows specific, but doing this saves startup time
            self.capture = cv.VideoCapture(camera_index, cv.CAP_DSHOW)
        else:
            self.capture = cv.VideoCapture(camera_index)

        # Check if camera stream could be opened/obtained
        if self.capture.isOpened():
            self.is_ready = True

    def is_ready(self) -> bool:
        return self.is_ready

    def end_capture(self):
        self.capture.release()

    def get_next_frame(self):
        # Capture frame-by-frame
        successful_capture, frame = self.capture.read()
        # if frame is read correctly ret is True
        if not successful_capture:
            print("Can't receive frame (stream end?). Exiting ...")

        # convert to float 32 type (with RGB values ranging from 0-255) - Because this is the only format dearpygui will take
        frame = np.float32(frame)
        frame /= 255.

        # convert to RGBA
        rgba_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)

        return rgba_frame

    def set_focus_callback(self, sender, data, user_data):
        # Sender is tag for UI element associated with this callback
        #   in this case the sender is the focus slider
        #   and the user data passed in is the tag for the autofocus checkbox
        new_focus_value = dpg.get_value(sender)
        AF_checkbox_tag = user_data
        # TODO Focus must be: min: 0, max: 255, increment:5?
        self.capture.set(cv.CAP_PROP_FOCUS, new_focus_value)
        # Uncheck DearPyGui's AutoFocus checkbox
        dpg.set_value(AF_checkbox_tag, value=False)

    def set_brightness_callback(self, sender, data, user_data):
        # Sender is tag for UI element associated with this callback
        #   in this case the sender is the brightness slider
        new_brightness_value = dpg.get_value(sender)
        # TODO check range (or make sure limits on slider are appropriate)
        # Set brightness value
        self.capture.set(cv.CAP_PROP_BRIGHTNESS, new_brightness_value)

    def reset_brightness_callback(self, sender, data, user_data):
        # Sender is tag for UI element associated with this callback
        #   in this case the sender is the reset brightness button
        #   and the user data passed in is the tag for the brightness slider
        brightness_slider_tag = user_data
        # Reset brightness to 0
        self.capture.set(cv.CAP_PROP_BRIGHTNESS, 0)
        # Update DearPyGUI's slider value to match
        dpg.set_value(brightness_slider_tag, value=0)

    def set_autofocus_callback(self, sender, data, user_data):
        # Sender is tag for UI element associated with this callback
        #   in this case the sender is the autofocus checkbox
        #   and the user data passed in is the tag for the autofocus slider
        self.AF_enabled = dpg.get_value(sender)
        focus_slider_tag = user_data

        if self.AF_enabled:
            # Update camera setting
            self.capture.set(cv.CAP_PROP_AUTOFOCUS, 1)
            # Set slider to 0
            dpg.set_value(focus_slider_tag, value=0)
            # Update slider enabled status
            # dpg.disable_item(focus_slider_tag)
        else:
            # Update camera setting
            self.capture.set(cv.CAP_PROP_AUTOFOCUS, 2)
            # Update slider enabled status
            # dpg.enable_item(focus_slider_tag)
