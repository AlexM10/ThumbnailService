class SizeHolder(object):


    """
        A class that holds the images size
        used for testing
    """
    def __init__(self, width, height):
        self.__width = width
        self.__height = height

    def get_size(self):
        return self.__width, self.__height




