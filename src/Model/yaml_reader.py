import yaml
from src.Model.config_reader import IConfigReader
from logger import Logger

"""
    A class that implements the ConfigReader interface for yaml files
"""


class YamlReader(IConfigReader):

    def __init__(self, logger: Logger):
        self.logger = logger

    def parse_file(self, path: str) -> dict:
        try:
            with open(path) as file:
                data = yaml.full_load(file)
            return data
        except (EnvironmentError, FileNotFoundError)as e:
            message = ("Failed to parse config.\n%s\n" % str(e))
            self.logger.write_to_log(message_to_write=message)
            return None
