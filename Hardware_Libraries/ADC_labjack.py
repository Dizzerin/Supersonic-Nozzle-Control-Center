from LabJackPython import LabJackException
from Interfaces.ADC_data_provider_interface import IADCDataProvider
from Temp_Interfaces import custom_types
from datetime import datetime, timedelta
import ue9
import numpy as np


class Ue9LabJackADC(IADCDataProvider):
    def __init__(self):
        # Call super class's init
        super(Ue9LabJackADC, self).__init__()

        # Local vars
        self.is_initialized = False
        self.is_calibrated = False
        self.device = None

        # Configurable parameters
        self.acquisition_start_time = None  # Set when data acquisition begins (roughly when the user first enters the live view mode)
        # TODO decide how to make the sampling rate configurable and consistent?
        # TODO make it so below is configurable and read from config file or something
        self.input_map = {  # Maps the inputs to the inputs on the ADC
            "t0": 0,
            "p0": 1,
            "p1": 2,
            "p2": 3,
            "p3": 4,
            "p4": 5
        }

        # Computed/read values
        self.atmospheric_psi = 14.26  # (P_atm in documentation, units: psi, defaults to avg pressure at 800ft)
        self.adc_offsets = np.array([0.0, 0.0, 0.0, 0.0, 0.0])  # (ba in documentation, units: V)

        # Stored offsets and gains
        self.adc_gains = np.array([0.049094016,  # (ma in documentation, units: V/mv)
                                   0.048944909,
                                   0.049298768,
                                   0.049041140,
                                   0.048913343
                                   ])
        self.sensor_offsets = np.array([-0.006,  # (bs in documentation, units: mV)
                                        0.0180,
                                        0.0220,
                                        -0.206,
                                        0.0140
                                        ])
        self.sensor_gains = np.array([0.100665,  # (ms in documentation, units: mV/psi)
                                      0.100508,
                                      0.200050,
                                      1.003380,
                                      2.019160
                                      ])

    def initialize(self):
        # Initialize LabJack ADC
        try:
            self.device = ue9.UE9()
        except LabJackException as exception:
            self.is_initialized = False
        else:
            # Temp calibrate with estimated default calibration value so live data can be displayed before actual
            # calibration takes place
            self.calibrate(self.atmospheric_psi)
            # Manually reset is_calibrated to false since official calibration hasn't taken place
            self.is_calibrated = False

            # Update initialized status var
            self.is_initialized = True

    def is_initialized(self) -> bool:
        return self.is_initialized

    def is_calibrated(self) -> bool:
        # TODO check that this is true before recording data
        return self.is_calibrated

    def calibrate(self, atmospheric_psi: float):
        # Use the given atmospheric pressure to calculate the proper adc_offsets

        # Store atmospheric_pressure
        self.atmospheric_psi = atmospheric_psi

        # Get current adc readings
        raw_adc_readings = self._get_raw_readings()

        # Compute adc offsets
        self.adc_offsets = self.adc_gains * (raw_adc_readings[1:] / self.adc_gains - (
                self.sensor_gains * self.atmospheric_psi + self.sensor_offsets))

        # TODO compute adc_offset for temperature as well

        # Update calibration status var
        self.is_calibrated = True

    def set_acquisition_start_time(self):
        self.acquisition_start_time = datetime.now()

    def _get_raw_readings(self):
        # (V in documentation, units: V, order: t0, p0, p1, p2 p3, p4)
        # Read raw data from the device (order: t0, p0, p1, p2 p3, p4)
        return [self.device.getAIN(self.input_map["t0"]),
                self.device.getAIN(self.input_map["p0"]),
                self.device.getAIN(self.input_map["p1"]),
                self.device.getAIN(self.input_map["p2"]),
                self.device.getAIN(self.input_map["p3"]),
                self.device.getAIN(self.input_map["p4"])
                ]

    def _convert_raw_readings(self, raw_adc_readings) -> custom_types.SensorData:
        # Converted data (units: deg celsius, psi, psi, psi, psi, psi)
        converted_pressures = ((raw_adc_readings[1:] - self.adc_offsets) / self.adc_gains - self.sensor_offsets) / (
            self.sensor_gains)

        # TODO convert first sensor reading as well which is the temperature

        # Store the final converted data in a SensorData object
        sensor_data = custom_types.SensorData(raw_adc_readings[0],
                                              converted_pressures[0],
                                              converted_pressures[1],
                                              converted_pressures[2],
                                              converted_pressures[3],
                                              converted_pressures[4],
                                              )
        return sensor_data

    def get_next_data_row(self) -> custom_types.SensorData:
        # Read raw data from the device
        raw_adc_readings = self._get_raw_readings()

        # Convert and return data
        return self._convert_raw_readings(raw_adc_readings)
