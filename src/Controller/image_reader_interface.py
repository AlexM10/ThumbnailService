import abc
from PIL import Image


class IImageReader(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'read_image') and
                callable(subclass.read_image) or
                NotImplemented)

    @abc.abstractmethod
    def read_image(self, path: str) -> Image:
        """reads the image from path and return a PIL image object"""
        raise NotImplementedError
