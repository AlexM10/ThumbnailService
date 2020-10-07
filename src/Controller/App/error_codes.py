from enum import IntEnum

"""
    Enum for server error handling
"""


class ServerErrorsCodes(IntEnum):
    BAD_URL = 400
    UNEXPECTED_ERROR = 500
    PRECONDITION_FAILED = 422
    REQUESTED_URL_NOT_FOUND = 404


"""
    A factory function which respond accordingly to 
    the given error
"""
class ResponseFactory(object):

    def getResponse(self, code):
        if code == ServerErrorsCodes.BAD_URL:
            return {
                'success': False,
                'error': {
                    'type': 'Bad URL',
                    'message': 'The Given URL corrupted or not an Image.',
                    'error_code': code
                }
            }

        elif code == ServerErrorsCodes.PRECONDITION_FAILED:
            return {
                'success': False,
                'error': {
                    'type': 'Precondition failed',
                    'message': 'A parameter in the query string contains an invalid or missing value.',
                    'error_code': code
                }
            }
        elif code == ServerErrorsCodes.REQUESTED_URL_NOT_FOUND:
            return {
                'success': False,
                'error': {
                    'type': 'Not found',
                    'message': 'The server encountered an unexpected condition which prevented it from fulfilling the request.',
                    'error_code': code
                }
            }
        else:
            return {
                'success': False,
                'error': {
                    'type': 'Unexpected_error',
                    'message': 'unexpected exception has occurred.',
                    'error_code': code
                }
            }
