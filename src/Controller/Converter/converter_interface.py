import abc
from PIL import Image


class IConverter(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'convert') and
                callable(subclass.convert) or
                NotImplemented)

    @abc.abstractmethod
    def convert(self, given_img: Image, target_width: int, target_height: int) -> Image:
        """manipulates image size and properties and returns a new Image object"""
        raise NotImplementedError
