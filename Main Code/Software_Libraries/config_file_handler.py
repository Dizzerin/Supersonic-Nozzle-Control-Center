import os.path

from Software_Interfaces.config_handler_interface import IConfigHandler
from Custom_Types.custom_types import TemperatureSensorConfigData, PressureSensorConfigData, ValidADCInputs, ConfigSettings, ValidSensorTypes
import configparser
from typing import List


# TODO (skip) make this so when it saves/writes a file it retain comments that were in it originally if possible somehow
# TODO (skip) Maybe make everything more dynamic based off the information this returns
#  i.e. the number of sensors etc.
# TODO (skip) Note: should re-read file without writing it if setting are not applied, otherwise the settings that were changed
#            will remain a part of this class and get handed around but be incorrect because the user didn't actually
#           chose to save the changes.


class ConfigHandler(IConfigHandler):
    def __init__(self, config_filepath: str):
        # Call super class's init
        super(ConfigHandler, self).__init__()

        # Local vars
        self._config_filepath = config_filepath
        self._config = configparser.ConfigParser()

        # Config values
        # Note: Most config data is stored in the self._config object and dynamically changed there etc.
        self._temperature_sensor_list = []
        self._pressure_sensor_list = []

        """
        Note: the following lines can throw exceptions if the file doesn't exist or the sections don't exist
        These exceptions need to be caught and handled outside this class
        
        Possible Exceptions:
            KeyError -- if a section is not found
            configparser.NoSectionError -- if a section is not found
            configparser.NoOptionError -- if a key/option within a section is not found
            ValueError -- if a type conversion cannot be made (i.e. getboolean with a long string or something)
        
        Configparser API notes:

        DO USE:
        config.get("Section", "key")            <-- this will raise a configparser.NoSectionError exception if the section is not found
        config.get("Section", "key")            <-- this will raise a configparser.NoOptionError exception if the key is not found
        (getint, getboolean, getfloat etc. all operate the same at this level)
        config.set("Section", "key", "value")   <-- this will raise a configparser.NoSectionError exception if the section is not found (no error if key not found)
        
        DECIDED NOT TO USE:
        config["Section"]["key"]                <-- this will raise a KeyError if the section or key are not found
        config["Section"]["key"] = "value"      <-- this will raise a KeyError is the section is not found (no error if key not found)
        
        DON'T USE:
        my_section = config["Section"]          <-- this will raise KeyError if the section is not found
        my_section.get("key")                   <-- this will not raise any exceptions if the key is not found, it will just return none
        (getint, getboolean, getfloat etc. all operate the same at this level)
        my_section.set("key", "value")          <-- this will not raise any exceptions if the key is not found, it will just return none
        my_section["key"]                       <-- this will raise a KeyError if the key is not found

        For sake of consistency, I chose to use the config.get or config.set syntax throughout as this syntax
        explicitly raises configparser.NoSectionError and configparser.NoOptionError exceptions when appropriate and
        it has handy type conversion aliases such as getboolean (which is different/safer than casting to a bool).
        (DO NOT USE the fancy my_section = config["Section"] and following section accessing and setting 
        methods as these do not raise exceptions!) 
        """

        # Verify config file exists
        if not os.path.isfile(self._config_filepath):
            raise Exception(f"Config file \"{self._config_filepath}\" could not be found.")

        # Try to read config file (could throw exception)
        # Open and read the file
        # (This will return an empty list if the file couldn't be read or found)
        self._config.read(self._config_filepath)

        # Read and parse the general section in the file
        # (this is done to verify the expected section and keys exist in the config file)
        self._config.get("General", "default_save_directory").strip('"')
        self._config.getint("General", "default_camera_index")
        self._config.getint("General", "camera_width")
        self._config.getint("General", "camera_height")
        self._config.getint("General", "camera_height")

        # Read and parse each of the following pressure and temperature sections
        for section in self._config.sections():
            if section.lower() == "general":
                pass
            else:
                # Get sensor type (and cast to ValidSensorTypes)
                try:
                    # (This will raise a ValueError exception if the cast cannot be made)
                    sensor_type = ValidSensorTypes(self._config.get(section, "type"))
                except ValueError as exception:
                    raise ValueError("Invalid sensor type specified in config file! {} is not one of {}".format(
                                        self._config.get(section, "type"), [e.value for e in ValidSensorTypes]))

                # If it's a temperature sensor...
                if sensor_type == ValidSensorTypes.temperature_sensor:
                    # Create temperature sensor object and add it to local list
                    self._temperature_sensor_list.append(TemperatureSensorConfigData(name=section.upper(),
                                                                                     descr_string=self._config.get(section, "description_string"),
                                                                                     adc_input=ValidADCInputs(self._config.get(section, "adc_input")),
                                                                                     amplifier_gain=self._config.getfloat(section, "amplifier_gain")))

                # Else if its a pressure sensor...
                elif sensor_type == ValidSensorTypes.pressure_sensor:
                    # Create pressure sensor object and add it to local list
                    self._pressure_sensor_list.append(PressureSensorConfigData(name=section.upper(),
                                                                               descr_string=self._config.get(section, "description_string"),
                                                                               adc_input=ValidADCInputs(self._config.get(section, "adc_input")),
                                                                               amplifier_gain=self._config.getfloat(section, "amplifier_gain"),
                                                                               sensor_gain=self._config.getfloat(section, "sensor_gain"),
                                                                               sensor_offset=self._config.getfloat(section, "sensor_offset")))
                else:
                    # Should NEVER reach this point even if and invalid type is specified because the cast should
                    # fail above and an exception should be thrown at that point
                    raise Exception("Cast to ValidSensorType failed and prior exception was ignored")

    def get_default_save_directory(self) -> str:
        return self._config.get("General", "default_save_directory").strip('"')

    def get_default_camera_index(self) -> int:
        return self._config.getint("General", "default_camera_index")

    def get_camera_width(self) -> int:
        return self._config.getint("General", "camera_width")

    def get_camera_height(self) -> int:
        return self._config.getint("General", "camera_height")

    def get_pressure_sensors(self) -> List[PressureSensorConfigData]:
        return self._pressure_sensor_list

    def get_temperature_sensors(self) -> List[TemperatureSensorConfigData]:
        return self._temperature_sensor_list

    def set_default_save_directory(self, filepath: str):
        self._config.set("General", "default_save_directory", str(filepath))

    def set_default_camera_index(self, index: int):
        self._config.set("General", "default_camera_index", str(index))

    def set_camera_width(self, width: int):
        self._config.set("General", "camera_width", str(width))

    def set_camera_height(self, height: int):
        self._config.set("General", "camera_height", str(height))

    def set_pressure_sensor(self, pressure_sensor: PressureSensorConfigData):
        # This function replaces the pressure sensor currently in self._pressure_sensor_list that has the same
        # name as the one being passed in with the one being passed in

        # Note:
        #   One should never need to add an additional pressure sensor (only update values on existing
        #   pressure sensors) as there is no reason an additional sensor would need to be added, but, if
        #   that was necessary for some reason, it can be done by directly editing the config file

        # Ensure name is upper case (force it to all upper)
        pressure_sensor.name = pressure_sensor.name.upper()

        # Locate the corresponding pressure sensor in the local list and replace it with this pressure sensor
        for i, p_sensor in enumerate(self._pressure_sensor_list):
            if p_sensor.name == pressure_sensor.name:
                self._pressure_sensor_list[i] = pressure_sensor

        # Also update the corresponding values in the config object
        self._config.set(pressure_sensor.name, "type", str(ValidSensorTypes.pressure_sensor.value))
        self._config.set(pressure_sensor.name, "description_string", pressure_sensor.descr_string)
        self._config.set(pressure_sensor.name, "adc_input", str(pressure_sensor.adc_input.value))
        self._config.set(pressure_sensor.name, "amplifier_gain", str(pressure_sensor.amplifier_gain))
        self._config.set(pressure_sensor.name, "sensor_gain", str(pressure_sensor.sensor_gain))
        self._config.set(pressure_sensor.name, "sensor_offset", str(pressure_sensor.sensor_offset))

    def set_temperature_sensor(self, temperature_sensor: TemperatureSensorConfigData):
        # This function replaces the temperature sensor currently in self._temperature_sensor_list that has the same
        # name as the one being passed in with the one being passed in and also updates the corresponding data in
        # the config object

        # Note:
        #   One should never need to add an additional temperature sensor (only update values on existing
        #   temperature sensors) as there is no reason an additional sensor would need to be added, but, if
        #   that was necessary for some reason, it can be done by directly editing the config file

        # Ensure name is upper case (force it to all upper)
        temperature_sensor.name = temperature_sensor.name.upper()

        # Locate the corresponding temperature sensor in the local list and replace it with this temperature sensor
        for i, t_sensor in enumerate(self._temperature_sensor_list):
            if t_sensor.name == temperature_sensor.name:
                self._temperature_sensor_list[i] = temperature_sensor

        # Also update the corresponding values in the config object
        self._config.set(temperature_sensor.name, "type", str(ValidSensorTypes.temperature_sensor.value))
        self._config.set(temperature_sensor.name, "description_string", temperature_sensor.descr_string)
        self._config.set(temperature_sensor.name, "adc_input", str(temperature_sensor.adc_input.value))
        self._config.set(temperature_sensor.name, "amplifier_gain", str(temperature_sensor.amplifier_gain))

    def set_config_settings(self, config_settings: ConfigSettings):
        # Updates all config settings
        self.set_default_camera_index(config_settings.default_camera_index)
        self.set_camera_width(config_settings.camera_width)
        self.set_camera_height(config_settings.camera_height)
        self.set_default_save_directory(config_settings.default_save_directory)

        for p_sensor in config_settings.pressure_sensor_list:
            self.set_pressure_sensor(p_sensor)

        for t_sensor in config_settings.temperature_sensor_list:
            self.set_temperature_sensor(t_sensor)

    def write_config_file(self):
        # Todo (skip) report success/failure and/or handle errors?
        with open(self._config_filepath, 'w') as ConfigFileHandle:
            self._config.write(ConfigFileHandle)
