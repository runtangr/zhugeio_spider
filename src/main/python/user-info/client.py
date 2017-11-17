#encoding=utf-8
'''
definition decorator
'''

import requests

__author__ = "tangr"

class Error(Exception):
    def __init__(self, code, error):
        self.code = code
        self.error = error

    def __str__(self):
        error = self.error if isinstance(self.error, str) else self.error.encode('utf-8', 'ignore')
        return 'Error: [{0}] {1}'.format(self.code, error)

def check_error(func):
    def new_func(*args, **kwargs):
        response = func(*args, **kwargs)
        assert isinstance(response, requests.Response)
        if response.headers.get('Content-Type') == 'text/html':
            raise Error(-1, 'Bad Request')

        content = response.json()

        if 'error' in content:
            raise Error(content.get('code', 1), content.get('error', 'Unknown Error'))

        return response
    return new_func