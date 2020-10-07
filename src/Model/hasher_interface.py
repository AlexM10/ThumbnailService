import abc


class Hasher(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'hash_data') and
                callable(subclass.hash_data) or
                NotImplemented)

    @abc.abstractmethod
    def hash_data(self, data_to_hash: tuple) -> int:
        """calculate the hash value of a data"""
        raise NotImplementedError
