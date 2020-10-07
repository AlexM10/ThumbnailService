from flask import Blueprint

from src.Controller.image_reader_url import ImageReaderUrl
from src.Controller.Converter.converter import ToThumbNailConverter
from src.Model.thumbnail_hasher import ThumbnailHasher
from src.Model.thumbnail_data_manager import ThumbnailDataManager
from src.Controller.image_utils import ImageUtils
from logger import Logger
from src.Controller.App.error_codes import ResponseFactory


"""
    A class that inherits from blue print 
    and save thumbnail service's operating
    objects
"""

class ThumbnailBlueprint(Blueprint):

    def __init__(self, name, prefix):
        super().__init__(name=name, import_name=__name__, url_prefix=prefix)
        self.utils = ImageUtils()
        self.data_manager = ThumbnailDataManager(logger=Logger("thumbnail_logger.txt"), img_utils=self.utils)
        self.converter = ToThumbNailConverter()
        self.hasher = ThumbnailHasher()
        self.error_responses = ResponseFactory()
        self.image_reader = ImageReaderUrl('JPEG', 'RGB')


