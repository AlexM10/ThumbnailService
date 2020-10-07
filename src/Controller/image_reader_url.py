from src.Controller.image_reader_interface import IImageReader
from PIL import Image
from io import BytesIO
import requests

"""
    A class that extends the Image Reader interface
"""


class ImageReaderUrl(IImageReader):

    def __init__(self, img_format, color):
        self.format = img_format
        self.color = color

    """
        Private function that transforms the image
        format and color settings to the given 
        settings.
    """
    def __fix_image(self, img):
        img = img.convert(self.color)
        img_io = BytesIO()
        img.save(img_io, self.format)
        img_io.seek(0)
        return Image.open(img_io)

    """
       Private function that reads 
       from url
    """
    def __read_from_url(self, image_url: str):
        return requests.get(image_url).content

    """
        The implementation of the read_image function
        as described in the interface 
    """
    def read_image(self, path: str) -> Image:
        return self.__fix_image(Image.open(BytesIO(self.__read_from_url(path))))
