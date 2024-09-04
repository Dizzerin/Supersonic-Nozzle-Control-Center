from Hardware_Interfaces.ADC_data_writer_interface import IADCDataWriter
from Custom_Types.custom_types import SensorData, SensorDataTimed
from datetime import datetime, timedelta  # TODO remove the last thing here if it remains unused
import csv


class ADCDataFileWriter(IADCDataWriter):
    def __init__(self, file):
        # Call super class's init
        super(ADCDataFileWriter, self).__init__(file)

        # Local vars
        self.file_writer = None

        # Attempt to create and open file
        # Add .csv extension if its not there
        if not self.file.endswith('.csv'):
            self.file += '.csv'
        # Create/open output file
        self.output_file = open(self.file, mode='w', newline='')
        # Create csv file writer object
        self.file_writer = csv.writer(self.output_file, dialect='excel', delimiter=',', quotechar='"',
                                      quoting=csv.QUOTE_MINIMAL)
        # Attempt to write header line in file
        self.file_writer.writerow(["Time (s)", "Elapsed Time (s)", "T0 (°C)", "P0 (PSI)", "P1 (PSI)", "P2 (PSI)", "P3 (PSI)", "P4 (PSI)"])

    def write_ADC_data(self, sensor_data_timed: SensorDataTimed):
        # Throw error if file writer is not set yet
        if self.file_writer is None:
            raise Exception("Error, filer_writer is invalid, cannot write file")

        sensor_data = sensor_data_timed.sensor_data

        self.file_writer.writerow(
            [sensor_data_timed.absolute_time.isoformat(), sensor_data_timed.elapsed_time, sensor_data.t0, sensor_data.p0, sensor_data.p1, sensor_data.p2, sensor_data.p3,
             sensor_data.p4])

    def close_file(self):
        self.output_file.close()
