from Software_Interfaces.config_handler_interface import IConfigHandler
from Custom_Types.custom_types import TemperatureSensorConfigData, PressureSensorConfigData, ValidADCInputs, \
    ConfigSettings, ValidSensorTypes
import configparser
from typing import List


# TODO implement use of this!!! Also maybe make everything more dynamic based off the information this returns
#  i.e. the number of sensors etc.


class INIConfigHandler(IConfigHandler):
    def __init__(self, config_filepath: str):
        # Call super class's init
        super(INIConfigHandler, self).__init__()

        # Local vars
        self._config_filepath = config_filepath
        self._config = configparser.ConfigParser()

        # # Config values
        # Decided to let these be stored in the self._config object and dynamically changed there etc.
        # TODO create a read file function called at the start the populates all these fields
        #   and DO have local copies of everything in the config specified here in this class
        #   and ALWAYS and ONLY modify, change, and access these values in memory NOT the values
        #   in memory within the config object, that way there is consistency and we can specify how
        #   we want the data and objects to be represented.  So read all this stuff in upon initialization
        #   and then from then on, only return these self._ local copies and modify and set them
        #   and then when we write the file at the end, explicitly copy all these local variables out to the config
        #   object (set all the values on the config object according to these local vars) and then write the config
        #   object
        # self._default_camera_index = None
        # self._camera_width = None
        # self._camera_height = None
        # self._default_save_directory = None
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
        config.get("Section", "key")    <-- this will raise a configparser.NoSectionError exception if the section is not found
        config.get("Section", "key")    <-- this will raise a configparser.NoOptionError exception if the key is not found
        (getint, getboolean, getfloat etc. all operate the same at this level)
        config.set("Section", "key", "value")   <-- this will raise a configparser.NoSectionError exception if the section is not found (no error if key not found)
        
        DECIDED NOT TO USE:
        config["Section"]["key"]        <-- this will raise a KeyError if the section or key are not found
        config["Section"]["key"] = "value"      <-- this will raise a KeyError is the section is not found (no error if key not found)
        
        DON'T USE:
        my_section = config["Section"]  <-- this will raise KeyError if the section is not found
        my_section.get("key")           <-- this will not raise any exceptions if the key is not found, it will just return none
        (getint, getboolean, getfloat etc. all operate the same at this level)
        my_section.set("key", "value")  <-- this will not raise any exceptions if the key is not found, it will just return none
        my_section["key"]               <-- this will raise a KeyError if the key is not found

        For sake of consistency, I chose to use the config.get or config.set syntax throughout as this syntax
        explicitly raises configparser.NoSectionError and configparser.NoOptionError exceptions when appropriate and
        it has handy type conversion aliases such as getboolean (which is different/safer than casting to a bool).
        (DO NOT USE the fancy my_section = config["Section"] and following section accessing and setting 
        methods as these do not raise exceptions!) 
        """

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
                    self.
                    TemperatureSensorConfigData(name=section,
                                                descr_string=,
                                                adc_input=,
                                                amplifier_gain=)

                # Else if its a pressure sensor...
                else:
                    # Create pressure sensor object and add it to local list

    def get_default_save_directory(self) -> str:
        return self.general_section.get("default_save_directory").strip('"')

    def get_default_camera_index(self) -> int:
        return self.general_section.getint("default_camera_index")

    def get_camera_width(self) -> int:
        return self.general_section.getint("camera_width")

    def get_camera_height(self) -> int:
        return self.general_section.getint("camera_height")

    def get_pressure_sensors(self) -> List[PressureSensorConfigData]:

    def get_temperature_sensors(self) -> List[TemperatureSensorConfigData]:

    def set_default_save_directory(self, filepath: str):
        self.general_section["default_save_location"] = str(filepath)

    def set_default_camera_index(self, index: int):
        self.general_section["default_camera_index"] = str(index)

    def set_camera_width(self, width: int):
        self.general_section["camera_width"] = str(width)

    def set_camera_height(self, height: int):
        self.general_section["camera_height"] = str(height)

    def set_pressure_sensor(self, pressure_sensor: PressureSensorConfigData):

    def set_temperature_sensor(self, temperature_sensor: TemperatureSensorConfigData):

    def set_config_settings(self, config_settings: ConfigSettings):

    def write_config_file(self):
        # Todo report success/failure and/or handle errors?
        with open(self._config_filepath, 'w') as ConfigFileHandle:
            self._config.write(ConfigFileHandle)
