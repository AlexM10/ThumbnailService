from src.Controller.Converter.dimension_holder import DimensionHolder
from src.Controller.Converter.image_dimension_calculator_interface import ImageDimensionCalculatorInterface

"""
    A class that calculate the dimension 
"""


class ThumbnailDimensionCalculator(ImageDimensionCalculatorInterface):
    """Calculated the ratio that needs to be saved"""

    def __calculate_ratio(self, dimensions: DimensionHolder) -> int:
        return min(dimensions.get_target_width() / dimensions.get_org_width(),
                   dimensions.get_target_height() / dimensions.get_org_height())

    """Calculated the new dimensions"""

    def calculate_new_dimensions(self, dimensions: DimensionHolder) -> (int, int):
        ratio = self.__calculate_ratio(dimensions=dimensions)
        new_height = int((float(dimensions.get_org_height()) * float(ratio)))
        new_width = int((float(dimensions.get_org_width()) * float(ratio)))
        return new_width, new_height
