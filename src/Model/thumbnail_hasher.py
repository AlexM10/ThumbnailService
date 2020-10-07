import imagehash
from src.Model.hasher_interface import Hasher
from PIL import Image

"""
    A Class that creates hash value for data of type
    [image:Image, width:int, height:int]
"""
class ThumbnailHasher(Hasher):

    def __hash_image(self, img_to_hash_on: Image) -> int:
        return imagehash.average_hash(img_to_hash_on)

    def hash_data(self, data_to_hash: list) -> int:
        if len(data_to_hash) == 3:
            hashed_image = self.__hash_image(data_to_hash[0])
            data = (hashed_image, data_to_hash[1], data_to_hash[2])
            return hash(tuple(data))
        else:
            return -1
