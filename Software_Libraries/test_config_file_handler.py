from unittest import TestCase
from Custom_Types.custom_types import *
from Software_Libraries.config_file_handler import ConfigHandler


# Quick file to run some basic test -- not full coverage
# TODO write this so it has more coverage
# TODO Note: Should not be able to add pressure sensors with new names (section must already exist in file)
# TODO Note: Pressure sensor names should be UPPER CASE


class TestConfigFileHandler(TestCase):
    def test_config_handler(self):
        # Create config handler class
        cfh = ConfigHandler("../config2.cfg")

        # Test reading in some data
        pressure_sensors = cfh.get_pressure_sensors()
        p0_original = pressure_sensors[0]
        temperature_sensors = cfh.get_temperature_sensors()
        width_original = cfh.get_camera_width()

        # Test setting some data
        width_test = 200
        cfh.set_camera_width(width_test)
        p0_test = PressureSensorConfigData(name="P0",
                                           descr_string="test",
                                           adc_input=ValidADCInputs("ADC13"),
                                           amplifier_gain=0.777,
                                           sensor_gain=0.333,
                                           sensor_offset=0.4444)
        cfh.set_pressure_sensor(p0_test)

        t0_test = TemperatureSensorConfigData(name="T0",
                                              descr_string="test2",
                                              adc_input=ValidADCInputs("ADC12"),
                                              amplifier_gain=0.737)
        cfh.set_temperature_sensor(t0_test)

        # Read back data, should be changed in memory
        pressure_sensors_after = cfh.get_pressure_sensors()
        p0_after = None
        for pressure_sensor in pressure_sensors_after:
            if pressure_sensor.name == p0_test.name:
                p0_after = pressure_sensor

        if p0_after is None:
            self.fail("{} was not found".format(p0_test.name))

        width_after = cfh.get_camera_width()

        # Assert changed data
        self.assertEqual(width_after, width_test, "Width did not get saved properly")
        self.assertEqual(p0_after, p0_test, "pressure sensor data was not updated properly")
        self.assertEqual(cfh.get_camera_width(), width_test)



        # Write the file
        cfh.write_config_file()


        # Read in changed data
        pressure_sensors_after = cfh.get_pressure_sensors()
        p0_after = None
        for pressure_sensor in pressure_sensors_after:
            if pressure_sensor.name == p0_test.name:
                p0_after = pressure_sensor

        if p0_after is None:
            self.fail("{} was not found".format(p0_test.name))

        width_after = cfh.get_camera_width()

        # Assert changed data
        self.assertEqual(width_after, width_test, "Width did not get saved properly")
        self.assertEqual(p0_after, p0_test, "Pressure data did not get saved properly")

        # Write original data back again
        cfh.set_camera_width(width_original)
        cfh.set_pressure_sensor(p0_original)

        # Write the file again
        cfh.write_config_file()
