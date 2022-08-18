from Interfaces.config_file_handler_interface import IConfigFileHandler
from Temp_Interfaces.custom_types import TemperatureSensorSettingsData, PressureSensorConfigData, SensorName, ADCInput
import configparser
from typing import List


class INIConfigFileHandler(IConfigFileHandler):
    def __init__(self, config_filepath: str):
        # Call super class's init
        super(INIConfigFileHandler, self).__init__(config_filepath)

        # Local vars
        self.config_file = config_filepath
        self.config = configparser.ConfigParser()

        # Try to read config file (could throw exception)
        # Todo make sure the exception is handled outside this class should this constructor fail
        self.config.read(self.config_file)

        # TODO handle errors if these sections can't be found?
        self.general_section = self.config["General"]
        self.adc_input_mapping_section = self.config["ADC Input Mapping"]
        self.amplifier_gains_section = self.config["Amplifier Gains"]
        self.sensor_gains_section = self.config["Sensor Gains"]
        self.sensor_offsets_section = self.config["Sensor Offsets"]
        self.description_strings_section = self.config["Description Strings"]

    def get_default_save_location(self) -> str:
        return self.general_section.get("default_save_location")

    def get_default_camera_index(self) -> int:
        return self.general_section.getint("default_camera_index")

    def get_camera_width(self) -> int:
        return self.general_section.getint("camera_width")

    def get_camera_height(self) -> int:
        return self.general_section.getint("camera_height")

    def get_pressure_sensors(self) -> List[PressureSensorConfigData]:
        # Create and return list of pressure sensors
        pressure_sensor_list = []

        for key in self.adc_input_mapping_section:
            # All pressure sensor names should be prefixed with "p"
            if key[0] == "p":
                pressure_sensor = PressureSensorConfigData(name=SensorName(key),
                                                           descr_string=self.description_strings_section.get(key),
                                                           adc_input=ADCInput(self.adc_input_mapping_section.get(key)),
                                                           amplifier_gain=self.amplifier_gains_section.getfloat(key),
                                                           sensor_gain=self.sensor_gains_section.getfloat(key),
                                                           sensor_offset=self.sensor_offsets_section.getfloat(key)
                                                           )
                # Add pressure sensor to list
                pressure_sensor_list.append(pressure_sensor)

        # Return list
        return pressure_sensor_list

    def get_temperature_sensors(self) -> List[TemperatureSensorSettingsData]:
        # Create and return list of pressure sensors
        temperature_sensor_list = []

        for key in self.adc_input_mapping_section:
            # All temperature sensor names should be prefixed with "t"
            if key[0] == "t":
                temperature_sensor = TemperatureSensorSettingsData(name=SensorName(key),
                                                                   descr_string=self.description_strings_section.get(key),
                                                                   adc_input=ADCInput(self.adc_input_mapping_section.get(key)),
                                                                   amplifier_gain=self.amplifier_gains_section.getfloat(key)
                                                                   )
                # Add pressure sensor to list
                temperature_sensor_list.append(temperature_sensor)

        # Return list
        return temperature_sensor_list

    def set_default_save_location(self, filepath: str):
        self.general_section["default_save_location"] = filepath

    def set_default_camera_index(self, index: int):
        self.general_section["default_camera_index"] = str(index)

    def set_camera_width(self, width: int):
        self.general_section["camera_width"] = str(width)

    def set_camera_height(self, height: int):
        self.general_section["camera_height"] = str(height)

    def set_pressure_sensor(self, pressure_sensor: PressureSensorConfigData):
        self.adc_input_mapping_section[str(pressure_sensor.name)] = str(pressure_sensor.adc_input)
        self.amplifier_gains_section[str(pressure_sensor.name)] = str(pressure_sensor.amplifier_gain)
        self.sensor_gains_section[str(pressure_sensor.name)] = str(pressure_sensor.sensor_gain)
        self.sensor_offsets_section[str(pressure_sensor.name)] = str(pressure_sensor.sensor_offset)
        self.description_strings_section[str(pressure_sensor.name)] = str(pressure_sensor.descr_string)

    def set_temperature_sensor(self, temperature_sensor: TemperatureSensorSettingsData):
        self.adc_input_mapping_section[str(temperature_sensor.name)] = str(temperature_sensor.adc_input)
        self.amplifier_gains_section[str(temperature_sensor.name)] = str(temperature_sensor.amplifier_gain)
        self.description_strings_section[str(temperature_sensor.name)] = str(temperature_sensor.descr_string)

    def write_config_file(self):
        # Todo report success/failure and/or handle errors?
        with open(self.config_file, 'w') as ConfigFileHandle:
            self.config.write(ConfigFileHandle)
