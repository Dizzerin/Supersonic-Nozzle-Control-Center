from datetime import datetime
from datetime import timedelta
import ue9
import numpy as np
import pandas as pd

# This avoids pandas causing problems
import warnings

warnings.filterwarnings('ignore')

# Parameters
period = 0.5  # Sampling period in seconds
duration = 5 * 60  # Duration to take data during
filename = "test.xls"  # Name of file to save data to

# Names of headers for the exported file
header_titles = ["Time (s)",
                 "T0 (V)",  # Analog input 0
                 "P0 (V)",  # Analog input 1
                 "P1 (V)",  # Analog input 2
                 "P2 (V)",  # Analog input 3
                 "P3 (V)",  # Analog input 4
                 "P4 (V)"]  # Analog input 5

# Record sensor calibration constants
amplifier_gain = np.array([0.049094016,
                           0.048944909,
                           0.049298768,
                           0.04904114,
                           0.048913343
                           ])

sensor_gain = np.array([0.100665,
                        0.100508,
                        0.20005,
                        1.00338,
                        2.01916
                        ])

sensor_offset = np.array([-0.006,
                          0.018,
                          0.022,
                          -0.206,
                          0.014
                          ])

amplifier_offset = np.zeros_like(sensor_offset)

"""
Initialize variables
"""
# Set the sampling period based on prior input
sampling_period = timedelta(seconds=period)

# Initialize the device
try:
    device = ue9.UE9()
except:
    quit()

"""
Calibrate Sensors
"""
# Have the user calibrate the sensors by reading off atmospheric pressure
P_atm = float(input("Input the barometer pressure in millibars: ")) / 68.9475729318

V_cal = np.array([device.getAIN(1),
                  device.getAIN(2),
                  device.getAIN(3),
                  device.getAIN(4),
                  device.getAIN(5)])

amplifier_offset = amplifier_gain * (V_cal / amplifier_gain - (sensor_gain * P_atm + sensor_offset))
print(amplifier_offset)

"""
Record Data
"""
# Initialize timestamps
start_datetime = datetime.now()
current_datetime = start_datetime
last_datetime = current_datetime
time_elapsed = (current_datetime - start_datetime).total_seconds()

# Initialize array of data by grabbing the first datapoint
data_array = np.array([[time_elapsed,
                        device.getAIN(0),
                        device.getAIN(1),
                        device.getAIN(2),
                        device.getAIN(3),
                        device.getAIN(4),
                        device.getAIN(5)]])
# device.getAIN(0)/0.00494,
# ((device.getAIN(1)-ba[0])/ma[0]-bs[0])/ms[0],
# ((device.getAIN(2)-ba[1])/ma[1]-bs[1])/ms[1],
# ((device.getAIN(3)-ba[2])/ma[2]-bs[2])/ms[2],
# ((device.getAIN(4)-ba[3])/ma[3]-bs[3])/ms[3],
# ((device.getAIN(5)-ba[4])/ma[4]-bs[4])/ms[4],    ]])

# Collect data for the proscribed duration, or until the user quits the program
# Stores said data in an excel file every loop
while round(time_elapsed * 2, 0) / 2 < duration:

    # Grabs the current time and compares it to the last time data was recorded
    current_datetime = datetime.now()
    current_delta = current_datetime - last_datetime

    # Saves data at the proscribed intervals
    if current_delta >= sampling_period:
        time_elapsed = (current_datetime - start_datetime).total_seconds()

        # Grabs the data from the labjack and stores it in the data array
        raw_data = np.array([[time_elapsed,
                              device.getAIN(0),
                              device.getAIN(1),
                              device.getAIN(2),
                              device.getAIN(3),
                              device.getAIN(4),
                              device.getAIN(5)]])
        # raw_data = np.array([[  time_elapsed,
        # device.getAIN(0)/0.00494,
        # ((device.getAIN(1)-ba[0])/ma[0]-bs[0])/ms[0],
        # ((device.getAIN(2)-ba[1])/ma[1]-bs[1])/ms[1],
        # ((device.getAIN(3)-ba[2])/ma[2]-bs[2])/ms[2],
        # ((device.getAIN(4)-ba[3])/ma[3]-bs[3])/ms[3],
        # ((device.getAIN(5)-ba[4])/ma[4]-bs[4])/ms[4],    ]])
        data_array = np.append(data_array, raw_data, axis=0)

        # Marks that data has just been recorded
        last_datetime = datetime.now()

        # Saves the data in the Excel file with the proscribed file name
        converted_data = pd.DataFrame(data_array)
        converted_data.to_excel(filename, header=header_titles, index=False)
