from Interfaces.ADC_data_writer_interface import IADCDataWriter
from Temp_Interfaces import custom_types
from datetime import datetime, timedelta


class ADCDataFileWriter(IADCDataWriter):
    def __init__(self):
        # Call super class's init
        super(ADCDataFileWriter, self).__init__()

        # Local vars
        self.recording_start_time = None  # Set when data recording begins (when the user clicks the record button)

    def set_recording_start_time(self):
        self.recording_start_time = datetime.now()

    def do_stuff(self):
        # Throw error if acquisition time has not been set yet
        if self.acquisition_start_time is None:
            raise Exception("Error, acquisition time must be set")

        # Compute elapsed times
        current_time = datetime.now()
        elapsed_acquisition_time = current_time - self.acquisition_start_time
        if self.recording_start_time is None:
            elapsed_recording_time = timedelta(seconds=0)
        else:
            elapsed_recording_time = current_time - self.recording_start_time

        data_row = custom_types.SensorData(elapsed_acquisition_time.total_seconds(),
                                           elapsed_recording_time.total_seconds(),
                                           converted_data[0],
                                           converted_data[1],
                                           converted_data[2],
                                           converted_data[3],
                                           converted_data[4],
                                           converted_data[5]
                                           )
