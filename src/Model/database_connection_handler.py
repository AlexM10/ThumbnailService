from logger import Logger
from src.Model.yaml_reader import YamlReader
from pymongo import MongoClient, errors
import pathlib

"""
    A class that responsible for connection to the remote
    data base
"""


class DBConnectionHandler(object):

    def __init__(self, logger: Logger, uri: dict):
        self.logger = logger
        path = pathlib.Path(".env.yaml").parent.absolute()
        self.my_config = uri if uri is not None else YamlReader(self.logger).parse_file(str(path)+"/.env.yaml")
        self.collection = self.init_collection(self.my_config)

    """A function that sets up the data base endpoit"""
    def init_collection(self, config):
        cluster = self.try_mongodb_conn(config['mongo']) if config is not None else None
        db = cluster[config['data_base']] if cluster is not None else None
        collection = db[config['collection']] if db is not None else None
        return collection

    """A rapper function for the connection request to data base"""
    def try_mongodb_conn(self, password: str):
        try:
            connection = MongoClient(password)
            return connection
        except errors as e:
            self.logger.write_to_log("Failed to connect to db server.\n%s\n" % str(e))
            print("Could not connect to server: %s" % e)
            return None

    """A function that checks if there is no connection and then try to reconnect"""
    def reconnect_if_needed(self):
        if self.collection is None:
            self.collection = self.init_collection(self.my_config)

    """return the collection endpoint"""
    def get_collector_connection(self):
        return self.collection
