from datetime import datetime

"""
    A logger class that right the rejections and 
    exceptions of the service the the file with a
    time stamp.
"""


class Logger:

    def __init__(self, file):
        self.file = file

    def write_to_log(self, message_to_write):
        file = open(self.file, 'a+')
        file.write(message_to_write + " " + str(datetime.now()))
        file.close()
