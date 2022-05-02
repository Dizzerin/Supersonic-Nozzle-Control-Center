from dataclasses import dataclass
import datetime


@dataclass
class DataRow:
    """
    Structure defining the values contained in a data row
    Each row has a timestamp associated with it, a temperature, and a number of pressure readings
    p's are pressures
    t's are temperatures
    """
    time: datetime
    t0: float
    p0: float
    p1: float
    p2: float
    p3: float
    p4: float

