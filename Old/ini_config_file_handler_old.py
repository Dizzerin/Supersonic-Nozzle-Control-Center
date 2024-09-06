from Software_Interfaces.config_handler_interface import IConfigHandler
from Custom_Types.custom_types import TemperatureSensorConfigData, PressureSensorConfigData, SensorName, ADCInput, \
    ADCMapObj
import configparser
from typing import List

# TODO (skip) implement use of this!!! Also maybe make everything more dynamic based off the information this returns
#  i.e. the number of sensors etc. -- OR JUST REMOVE THE CONFIG AND SETTINGS FEATURE


class INIConfigHandler(IConfigHandler):
    def __init__(self, config_filepath: str):
        # Call super class's init
        super(INIConfigHandler, self).__init__()

        # Local vars
        self.config_file = config_filepath
        self.config = configparser.ConfigParser()

        """
        Note: the following lines can throw exceptions if the file doesn't exist or the sections don't exist
        These exceptions need to be caught and handled outside this class
        """
        # Try to read config file (could throw exception)
        # Open and read the file
        self.config.read(self.config_file)
        # Read the following sections in the file
        self.general_section = self.config["General"]
        self.adc_input_mapping_section = self.config["ADC Input Mapping"]
        self.amplifier_gains_section = self.config["Amplifier Gains"]
        self.sensor_gains_section = self.config["Sensor Gains"]
        self.sensor_offsets_section = self.config["Sensor Offsets"]
        self.description_strings_section = self.config["Description Strings"]

    def get_default_save_directory(self) -> str:
        return self.general_section.get("default_save_directory").strip('"')

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

    def get_temperature_sensors(self) -> List[TemperatureSensorConfigData]:
        # Create and return list of pressure sensors
        temperature_sensor_list = []

        for key in self.adc_input_mapping_section:
            # All temperature sensor names should be prefixed with "t"
            if key[0] == "t":
                temperature_sensor = TemperatureSensorConfigData(name=SensorName(key),
                                                                 descr_string=self.description_strings_section.get(key),
                                                                 adc_input=ADCInput(self.adc_input_mapping_section.get(key)),
                                                                 amplifier_gain=self.amplifier_gains_section.getfloat(key)
                                                                 )
                # Add pressure sensor to list
                temperature_sensor_list.append(temperature_sensor)

        # Return list
        return temperature_sensor_list

    def set_default_save_directory(self, filepath: str):
        self.general_section["default_save_directory"] = str(filepath)

    def set_default_camera_index(self, index: int):
        self.general_section["default_camera_index"] = str(index)

    def set_camera_width(self, width: int):
        self.general_section["camera_width"] = str(width)

    def set_camera_height(self, height: int):
        self.general_section["camera_height"] = str(height)

    def set_pressure_sensor(self, pressure_sensor: PressureSensorConfigData):
        self.adc_input_mapping_section[pressure_sensor.name.value] = pressure_sensor.adc_input.value
        self.amplifier_gains_section[pressure_sensor.name.value] = str(pressure_sensor.amplifier_gain)
        self.sensor_gains_section[pressure_sensor.name.value] = str(pressure_sensor.sensor_gain)
        self.sensor_offsets_section[pressure_sensor.name.value] = str(pressure_sensor.sensor_offset)
        self.description_strings_section[pressure_sensor.name.value] = pressure_sensor.descr_string

    def set_temperature_sensor(self, temperature_sensor: TemperatureSensorConfigData):
        self.adc_input_mapping_section[temperature_sensor.name.value] = temperature_sensor.adc_input.value
        self.amplifier_gains_section[temperature_sensor.name.value] = str(temperature_sensor.amplifier_gain)
        self.description_strings_section[temperature_sensor.name.value] = temperature_sensor.descr_string

    def set_adc_input(self, adc_map_obj: ADCMapObj):
        self.adc_input_mapping_section[adc_map_obj.sensor_name.value] = adc_map_obj.adc_input.value

    def write_config_file(self):
        # Todo (skip) report success/failure and/or handle errors?
        with open(self.config_file, 'w') as ConfigFileHandle:
            self.config.write(ConfigFileHandle)
