from Interfaces.ADC_data_provider_interface import IADCDataProvider
from Temp_Interfaces import custom_types
from datetime import datetime
import ue9


class Ue9LabjackADC(IADCDataProvider):
    def __init__(self):
        # Call super class's init
        super(Ue9LabjackADC, self).__init__()

        # Local vars
        self.is_ready = False
        self.device = None

    def initialize(self):
        # Initialize Labjack ADC
        self.device = ue9.UE9()
        # TODO properly check to see if the device was initialized and is ready
        self.is_ready = True

    def is_ready(self) -> bool:
        return self.is_ready

    def calibrate(self):
        # Todo
        pass

    def _convert_raw_data(self, data_array) -> custom_types.DataRow:
        # Todo -- convert raw data, make use of calibration offsets, etc.
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
        # Read raw data from the device
        # TODO make it so the ports to read from can be configured in a settings/config file
        raw_data = [self.device.getAIN(0),
                    self.device.getAIN(1),
                    self.device.getAIN(2),
                    self.device.getAIN(3),
                    self.device.getAIN(4),
                    self.device.getAIN(5)
                    ]

        # Convert and return data
        return self._convert_raw_data(raw_data)
