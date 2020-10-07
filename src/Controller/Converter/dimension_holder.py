from PIL import Image

"""
    A class that holds the dimension during conversion process
"""


class DimensionHolder(object):

    def __init__(self, img: Image, width: int, height: int):
        self.org_width = img.size[0]
        self.org_height = img.size[1]
        self.target_width = width
        self.target_height = height

    def get_org_width(self):
        return self.org_width

    def get_org_height(self):
        return self.org_height

    def get_target_width(self):
        return self.target_width

    def get_target_height(self):
        return self.target_height
