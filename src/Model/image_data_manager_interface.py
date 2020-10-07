import abc


class ImageDataManagerInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'put') and
                callable(subclass.put) and
                hasattr(subclass, 'retrieve') and
                callable(subclass.retrieve) and
                hasattr(subclass, 'is_exist') and
                callable(subclass.is_exist) or
                NotImplemented)

    @abc.abstractmethod
    def put(self, data_id: int, data) -> bool:
        """puts a data to the data base with data_id"""
        raise NotImplementedError

    @abc.abstractmethod
    def retrieve(self, data_id: int):
        """retrieves a data from data base with given data_id"""
        raise NotImplementedError

    @abc.abstractmethod
    def is_exist(self, img_id: int) -> bool:
        """returns true if a data record is exists in the data base"""
        raise NotImplementedError
