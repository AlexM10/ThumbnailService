from pymongo import errors
from src.Model.image_data_manager_interface import ImageDataManagerInterface
from src.Controller.image_utils import ImageUtils
from src.Model.database_connection_handler import DBConnectionHandler
from logger import Logger

""" 
    A ThumbnailDataManager that implements the ImageDataManager Interface
"""


class ThumbnailDataManager(ImageDataManagerInterface):

    def __init__(self, img_utils: ImageUtils, logger: Logger, **kwargs):
        self.utils = img_utils
        self.logger = logger
        uri = kwargs.get('uri', None)
        self.connection_handler = DBConnectionHandler(logger=logger, uri=uri)

    def collection(self):
        return self.connection_handler.get_collector_connection()

    def __create_record(self, data_id: int, image_bytes: object) -> dict:
        return {'_id': data_id, 'img': image_bytes}

    def put(self, data_id: int, data) -> bool:
        self.connection_handler.reconnect_if_needed()
        try:
            image_bytes = self.utils.image_to_bytes(data)
            self.collection().insert_one(self.__create_record(data_id=data_id, image_bytes=image_bytes))
            return True
        except (Exception, errors.PyMongoError) as e:
            self.logger.write_to_log("Failed to put to data_base record %s.\n%s\n" % (data_id, str(e)))
            return False

    def retrieve(self, data_id: int):
        self.connection_handler.reconnect_if_needed()
        try:
            img_data = self.collection().find_one(data_id)
            binary_img = img_data['img']
            return self.utils.bytes_to_bytesIO(binary_img)
        except (Exception, errors.PyMongoError) as e:
            self.logger.write_to_log("Failed to retrieve from data_base record %s.\n%s\n" % (data_id, str(e)))
            return None

    def is_exist(self, data_id) -> bool:
        self.connection_handler.reconnect_if_needed()
        try:
            ans = self.collection().find_one(data_id)
            return True if ans is not None else False
        except (Exception, errors.PyMongoError) as e:
            message = ("Failed to find a data_base record %s.\n%s\n" % (data_id, str(e)))
            self.logger.write_to_log(message_to_write=message)
            return False


"""
    A class that mocks the ThumbnailDataManager logic without the dependency
    of the data base
 """


class ThumbnailDataManagerTestLogic(ImageDataManagerInterface):

    def __init__(self, img_utils: ImageUtils, logger: Logger, **kwargs):
        self.utils = img_utils
        self.logger = logger
        self.collection = {}

    def collection(self):
        return self.collection

    def __create_record(self, data_id: int, image_bytes: object) -> dict:
        return {'_id': data_id, 'img': image_bytes}

    def put(self, data_id: int, data) -> bool:
        try:
            image_bytes = self.utils.image_to_bytes(data)
            self.collection[data_id] = self.__create_record(data_id=data_id, image_bytes=image_bytes)
            return True
        except (errors.PyMongoError, Exception) as e:
            self.logger.write_to_log("Failed to put to data_base record %s.\n%s\n" % (data_id, str(e)))
            return False

    def retrieve(self, data_id: int):
        try:
            img_data = self.collection[data_id]
            binary_img = img_data['img']
            return self.utils.bytes_to_bytesIO(binary_img)
        except (Exception, errors.PyMongoError) as e:
            self.logger.write_to_log("Failed to retrieve from data_base record %s.\n%s\n" % (data_id, str(e)))
            return None

    def is_exist(self, data_id) -> bool:
        try:
            if data_id in self.collection:
                return True
            else:
                return False
        except (Exception, errors.PyMongoError) as e:
            message = ("Failed to find a data_base record %s.\n%s\n" % (data_id, str(e)))
            self.logger.write_to_log(message_to_write=message)
            return False
