from dataclasses import dataclass
from enum import Enum
import datetime
from typing import List


@dataclass
class SensorData:
    """
    Structure defining all sensor data values
    This "struct" is used to house the final converted data read from the sensors using the ADC
    t is a temperature
    p's are pressures
    """
    t0: float
    p0: float
    p1: float
    p2: float
    p3: float
    p4: float


@dataclass
class SensorDataWriteRow:
    """
    Structure defining the values contained in a data row
    This "struct" is used to contain all the data associated with what gets written by the ADC data writer

    TODO may get rid of this, may not need it

    Each row has two timestamps associated with it, a temperature, and a number of pressure readings
    acquisition_elapsed_time is the time since the ADC began reporting data during the current session
    recording_elapsed_time is the time since the ADC data recording (writing to file etc.) began
    t is a temperature
    p's are pressures
    """
    acquisition_elapsed_time: datetime
    recording_elapsed_time: datetime
    t0: float
    p0: float
    p1: float
    p2: float
    p3: float
    p4: float


class ADCInput(Enum):
    # List of valid ADC inputs
    ADC0 = "ADC0"
    ADC1 = "ADC1"
    ADC2 = "ADC2"
    ADC3 = "ADC3"
    ADC4 = "ADC4"
    ADC5 = "ADC5"
    ADC6 = "ADC6"
    ADC7 = "ADC7"
    ADC8 = "ADC8"
    ADC9 = "ADC9"
    ADC10 = "ADC10"
    ADC11 = "ADC11"
    ADC12 = "ADC12"
    ADC13 = "ADC13"


class SensorName(Enum):
    # TODO DO AWAY WITH THIS
    # All possible valid sensor names (can add more here if more sensors are added later)
    # anything prefixed with "t" is a temperature sensor and anything prefixed with "p" is a pressure sensor
    # that affects the settings window
    t0 = "t0"
    p0 = "p0"
    p1 = "p1"
    p2 = "p2"
    p3 = "p3"
    p4 = "p4"


@dataclass
class PressureSensorConfigData:
    name: SensorName
    descr_string: str
    adc_input: ADCInput
    amplifier_gain: float
    sensor_gain: float
    sensor_offset: float


@dataclass
class TemperatureSensorConfigData:
    name: SensorName
    descr_string: str
    adc_input: ADCInput
    amplifier_gain: float


@dataclass
class ADCMapObj:
    # Maps a sensor to an ADC input
    sensor_name: SensorName
    adc_input: ADCInput


@dataclass
class ConfigSettings:
    # This object encapsulates all the data contained within the config/settings file
    # This is what the config handler ultimately reads and writes
    default_camera_index: int
    camera_width: int
    camera_height: int
    default_save_location: str
    temperature_sensor_list: List[TemperatureSensorConfigData]
    pressure_sensor_list: List[PressureSensorConfigData]


@dataclass
class SettingsObj:
    # TODO DO AWAY WITH THIS
    # This is what the settings window hands to the "OK" button callback
    default_camera_index: int
    camera_width: int
    camera_height: int
    default_save_location: str
    ADC_map_list: List[ADCMapObj]
