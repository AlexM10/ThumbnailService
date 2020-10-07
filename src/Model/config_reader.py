import abc



class IConfigReader(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'parse_file') and
                callable(subclass.parse_file) or
                NotImplemented)

    @abc.abstractmethod
    def parse_file(self, path: str):
        """Reads from config file"""
        raise NotImplementedError
