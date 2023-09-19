from Hardware_Interfaces.ADC_data_writer_interface import IADCDataWriter
from Custom_Types.custom_types import SensorData
from datetime import datetime, timedelta  # TODO remove the last thing here if it remains unused
import csv


class ADCDataFileWriter(IADCDataWriter):
    def __init__(self, file):
        # Call super class's init
        super(ADCDataFileWriter, self).__init__(file)

        # Local vars
        self.logging_start_time = None  # Set when data logging begins (when the user clicks the record button)
        self.file_writer = None

        # Attempt to create and open file
        # TODO Make sure we don't overwrite anything, handle errors when it can't be opened, etc. Use correct file, etc.
        #   add try catch?
        # TODO this should probably be done on a start logging function and saved and stopped on a stop logging
        #  function and we should have the ability to provide different filenames each time -- right now if one
        #  logging is started we can't start another one after the first one is stopped -- also we need the file name
        #  before we even get it I think... idk
        #  also we need to timestamp these files etc. maybe?
        self.output_file = open(self.file + '.csv', mode='w', newline='')
        # Create csv file writer object
        self.file_writer = csv.writer(self.output_file, dialect='excel', delimiter=',', quotechar='"',
                                      quoting=csv.QUOTE_MINIMAL)
        # Attempt to write header line in file
        self.file_writer.writerow(["Time (s)", "T0 (°C)", "P0 (PSI)", "P1 (PSI)", "P2 (PSI)", "P3 (PSI)", "P4 (PSI)"])

    def set_logging_start_time(self):
        self.logging_start_time = datetime.now()

    def write_ADC_data(self, sensor_data: SensorData, time_sample_was_taken: datetime):
        # Throw error if logging time has not been set yet
        if self.logging_start_time is None:
            raise Exception("Error, logging start time must be set before logging data")

        # Throw error if file writer is not set yet
        if self.file_writer is None:
            raise Exception("Error, filer_writer is invalid, cannot write file")

        # Compute elapsed time
        elapsed_logging_time = time_sample_was_taken - self.logging_start_time

        self.file_writer.writerow(
            [elapsed_logging_time.total_seconds(), sensor_data.t0, sensor_data.p0, sensor_data.p1, sensor_data.p2, sensor_data.p3,
             sensor_data.p4])

    def save_file(self):
        self.output_file.close()
