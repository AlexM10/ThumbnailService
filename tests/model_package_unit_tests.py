from mockupdb import go, MockupDB
from src.Model.thumbnail_data_manager import ThumbnailDataManagerTestLogic, ThumbnailDataManager
from src.Model.image_data_manager_interface import ImageDataManagerInterface
from src.Model.config_reader import IConfigReader
from src.Model.thumbnail_hasher import ThumbnailHasher
from src.Controller.image_utils import ImageUtils
from src.Model.yaml_reader import YamlReader
from src.Model.database_connection_handler import DBConnectionHandler
from logger import Logger
from PIL import Image
from pymongo import MongoClient, collection
import unittest

logger = Logger("logger.txt")

"""A function which reads reads the last n lines from file"""
def read_last_n_lines(file, n):
    with open(file) as file:
        ans = ""
        for line in (file.readlines()[-n:]):
            ans = ans + line + " "
        return ans[0:-2]


class YamlReaderTest(unittest.TestCase):

    def setUp(self) -> None:
        self.path = ".env_test.yaml"
        self.reader = YamlReader(logger=logger)

    """Checks if the file read successfully"""
    def test_yamlReader_implements_config_reader(self):
        ans = issubclass(self.reader, IConfigReader)
        self.assertEqual(ans, True)

    """checks if the the reader read the right fields"""
    def test_parse_file_right(self):
        ans = self.reader.parse_file(self.path)
        self.assertEqual(ans['mongo'], "mongo_read_success")
        self.assertEqual(ans['data_base'], "data_base_read_success")
        self.assertEqual(ans['collection'], "image_read_success")

    """checks that reader didnt read the right things"""
    def test_parse_file_wrong(self):
        ans = self.reader.parse_file(self.path)
        self.assertNotEqual(ans['mongo'], "mongo_rsead_success")
        self.assertNotEqual(ans['data_base'], "data_basdase_read_success")
        self.assertNotEqual(ans['collection'], "imasge_read_success")

    """Tests if that we go None when there is no file to read"""
    def test_no_file(self):
        ans = self.reader.parse_file("self.path")
        self.assertEqual(None, ans)


""" Can't check with time stamp on the logger
    def test_exceptions(self):
        self.reader.parse_file("self.path")
        ans = "Failed to parse config.\n [Errno 2] No such file or directory: \'self.path\'"
        self.assertEqual(read_last_n_lines('logger.txt', 2), ans)

"""


class HasherTest(unittest.TestCase):

    def setUp(self) -> None:
        self.img = Image.open("../tests/sample.jpg")
        self.hasher = ThumbnailHasher()

    """Test that the image was hashed"""
    def test_hash_image(self):
        ans = self.hasher._ThumbnailHasher__hash_image(self.img)
        self.assertEqual(str(ans), "12c89c3c3c3a0a18")

    """Tests that the data[img, width , height] was hashed"""
    def test_hash_data(self):
        ans = self.hasher.hash_data([self.img, 200, 200])
        self.assertEqual(str(ans), "-2709535219698968237")

    """test if changed order of data is different hash value"""
    def test_hash_diff(self):
        first = self.hasher.hash_data([self.img, 100, 200])
        second = self.hasher.hash_data([self.img, 200, 100])
        self.assertNotEqual(str(first), str(second))

    def tearDown(self) -> None:
        self.img.close()


class DBConnectionHandlerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.server = MockupDB(auto_ismaster={"maxWireVersion": 3})
        self.server.run()
        self.uri = {'mongo': self.server.uri, 'data_base': 'test_database', 'collection': 'test_collection'}
        self.handler = DBConnectionHandler(logger=logger, uri=self.uri)

    """Test if connected to mock data base"""
    def test_try_mongodb_conn(self):
        ans = self.handler.try_mongodb_conn(self.uri['mongo'])
        self.assertEqual(isinstance(ans, MongoClient), True)

    """Test if Connection has been established"""
    def test_init_collection(self):
        ans = self.handler.init_collection(self.uri)
        self.assertEqual(isinstance(ans, collection.Collection), True)

    """test if connections has failed"""
    def test_failed_init_connections(self):
        ans = self.handler.init_collection(None)
        self.assertEqual(ans, None)


class DataBaseManagerLogicTest(unittest.TestCase):

    def setUp(self) -> None:
        self.img = Image.open("../tests/sample.jpg")
        self.utils = ImageUtils()
        self.hasher = ThumbnailHasher()
        self.manager = ThumbnailDataManagerTestLogic(logger=logger, img_utils=self.utils)

    """Validates that thumbnail data manager implements image data_manager interface"""
    def test_thumbnail_data_manager_implements_image_data_manager_interface(self):
        ans_mongo = issubclass(ThumbnailDataManager, ImageDataManagerInterface)
        ans_test = issubclass(ThumbnailDataManagerTestLogic, ImageDataManagerInterface)
        self.assertEqual(ans_mongo, True)
        self.assertEqual(ans_test, True)

    """Test create record function"""
    def test_create_record(self):
        ans = self.manager._ThumbnailDataManagerTestLogic__create_record("1", "2")
        self.assertEqual(ans['_id'], "1")
        self.assertEqual(ans['img'], "2")

    """Tests put to database function logic"""
    def test_put_true(self):
        ans = self.manager.put(1, self.img)
        self.assertEqual(ans, True)

    """Test retrieve from data base function logic"""
    def test_retrieve(self):
        self.assertEqual(self.manager.put(1, self.img), True)
        bytes_image = self.utils.image_to_bytes(self.img)
        self.assertEqual(bytes_image, self.manager.retrieve(1).read())
        self.assertEqual(None, self.manager.retrieve(2))
        # message = "Failed to retrieve from data_base record 2.\n 2"
        # self.assertEqual(message, read_last_n_lines("logger.txt", 2)) cant check with time stamp on logger

    """Test if exist function logic"""
    def test_is_exist(self):
        self.assertEqual(self.manager.put(1, self.img), True)
        self.assertEqual(True, self.manager.is_exist(1))
        self.assertEqual(False, self.manager.is_exist(3))

    def tearDown(self) -> None:
        self.img.close()
