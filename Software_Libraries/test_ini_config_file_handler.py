from unittest import TestCase
from Temp_Interfaces.custom_types import *
from Software_Libraries.ini_config_file_handler import INIConfigHandler
# Quick file to run some basic test -- not full coverage


class TestINIConfigFileHandler(TestCase):
    def test_some_stuff(self):
        # Create config handler class
        cfh = INIConfigHandler("../config.cfg")

        # Test reading in some data
        pressure_sensors = cfh.get_pressure_sensors()
        p0_original = pressure_sensors[0]
        temperature_sensors = cfh.get_temperature_sensors()
        width_original = cfh.get_camera_width()

        # Test setting some data
        width_test = 200
        cfh.set_camera_width(width_test)
        p0_test = PressureSensorConfigData(name=SensorName("p0"),
                                           descr_string="test",
                                           adc_input=ADCInput("ADC13"),
                                           amplifier_gain=0.777,
                                           sensor_gain=0.333,
                                           sensor_offset=0.4444)
        cfh.set_pressure_sensor(p0_test)

        # Write the file
        cfh.write_config_file()

        # Read in changed data
        pressure_sensors_after = cfh.get_pressure_sensors()
        p0_after = None
        for i, pressure_sensor in enumerate(pressure_sensors_after):
            if pressure_sensor.name.value == "p0":
                p0_index = i
                p0_after = pressure_sensors_after[i]

        if p0_after is None:
            self.fail("p0 was not read from the config file")

        width_after = cfh.get_camera_width()

        # Assert changed data
        self.assertEqual(width_after, width_test, "Width did not get saved properly")
        self.assertEqual(p0_after, p0_test, "Pressure data did not get saved properly")

        # Write original data back again
        cfh.set_camera_width(width_original)
        cfh.set_pressure_sensor(p0_original)

        # Write the file again
        cfh.write_config_file()
