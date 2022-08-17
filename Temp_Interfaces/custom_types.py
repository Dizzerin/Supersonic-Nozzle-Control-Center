from dataclasses import dataclass
import datetime


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
