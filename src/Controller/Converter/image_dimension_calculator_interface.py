import abc
from src.Controller.Converter.dimension_holder import DimensionHolder


class ImageDimensionCalculatorInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'calculate_new_dimensions') and
                callable(subclass.calculate_new_dimensions) or
                NotImplemented)

    @abc.abstractmethod
    def calculate_new_dimensions(self, dimensions: DimensionHolder) -> (int, int):
        """calculate image's new dimensions"""
        raise NotImplementedError
