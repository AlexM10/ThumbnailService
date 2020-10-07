from src.Controller.Converter.image_dimension_calculator import ThumbnailDimensionCalculator
from src.Controller.Converter.dimension_holder import DimensionHolder
from src.Controller.Converter.converter_interface import IConverter
from PIL import Image

"""
    A class which implements the IConverter
    interface.
    Converts the image to thumbnail image.
"""


class ToThumbNailConverter(IConverter):

    def __init__(self):
        self.calculator = ThumbnailDimensionCalculator()

    """checks if the requested dimensions are not valid"""
    def __not_valid(self, dimensions: DimensionHolder) -> bool:
        return dimensions.get_org_height() < dimensions.get_target_height() \
               and dimensions.get_org_width() < dimensions.get_target_width()

    """Creates a black border for the image if needed"""
    def __create_thumbnail_with_borders(self, box_size: (int, int), image_size: (int, int), img: Image) -> Image:
        new_img = Image.new("RGB", box_size)
        new_img.paste(img, (int((box_size[0] - image_size[0]) / 2),
                            (int((box_size[1] - image_size[1]) / 2))))
        return new_img

    """Resizing the image to the requested dimensions"""
    def __resize_image(self, img: Image, dimensions: DimensionHolder) -> Image:
        if not self.__not_valid(dimensions):
            new_width, new_height = self.calculator.calculate_new_dimensions(dimensions)
            img = img.resize((new_width, new_height), Image.LANCZOS)
        return img

    """
        A function that endpoint function to convert the image to
        the requested dimensions
    """
    def convert(self, given_img: Image, target_width: int, target_height: int) -> Image:
        dimensions = DimensionHolder(img=given_img, width=target_width, height=target_height)
        img = self.__resize_image(img=given_img, dimensions=dimensions)
        return self.__create_thumbnail_with_borders(box_size=(target_width, target_height),
                                                    image_size=(img.size[0], img.size[1]), img=img)
