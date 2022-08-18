from abc import ABC, abstractmethod


class IConfigFileHandler(ABC):
    def __init__(self, config_filepath):
        self.config_file = config_filepath

    @abstractmethod
    def get_sections(self):
        pass

    @abstractmethod
    def get_int(self):
        pass

    @abstractmethod
    def get_float(self):
        pass

    @abstractmethod
    def get_string(self):
        pass

    @abstractmethod
    def get_bool(self):
        pass
