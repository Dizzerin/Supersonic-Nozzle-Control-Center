from Interfaces.ADC_data_provider_interface import IADCDataProvider
from Temp_Interfaces import custom_types
from datetime import datetime
import random
"""
This is a test data provider which implements the ADC Data Provider interface (IADCDataProvider)
This device can be supplied to the main application instead of the LabJack device or any other device
It simply returns randomized data values within a specified range

This class is used for testing purposes
"""


class ADCTestDevice(IADCDataProvider):
    def __init__(self):
        # Call super class's init
        super(ADCTestDevice, self).__init__()

        # Local vars
        self.is_ready = False

    def initialize(self):
        # Initialize Labjack ADC
        print("ADC initialization routine called")
        self.is_ready = True

    def is_ready(self) -> bool:
        return self.is_ready

    def calibrate(self):
        # TODO test calibration offsets etc.?
        print("ADC calibration routine called")

    def _convert_raw_data(self, data_array) -> custom_types.DataRow:
        # TODO test calibration offsets etc.?
        converted_data = custom_types.DataRow(datetime.now(),
                                              data_array[0],
                                              data_array[1],
                                              data_array[2],
                                              data_array[3],
                                              data_array[4],
                                              data_array[5]
                                              )
        return converted_data

    def get_next_data_row(self) -> custom_types.DataRow:
        # Return randomized data values
        raw_data = [random.randrange(0, 100),
                    random.randrange(0, 100),
                    random.randrange(0, 100),
                    random.randrange(0, 100),
                    random.randrange(0, 100),
                    random.randrange(0, 100)]

        # Convert and return data
        return self._convert_raw_data(raw_data)
