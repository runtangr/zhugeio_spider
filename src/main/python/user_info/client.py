# encode:utf-8

import requests
import json
import time
import os
from exception import LoginException
from config import LOGIN_URL, TOKEN_FILE

'''
user login and save token.
'''


class ZhugeToken:
    def __init__(self, success, user):
        self.create_at = time.time()
        self.user = user
        self.success = success

    @classmethod
    def from_file(cls, filename):
        with open(filename) as f:
            return cls.from_dict(json.load(f))

    @staticmethod
    def save_file(filename, data):
        with open(filename, 'w') as f:
            json.dump(data, f, ensure_ascii=False)

    @classmethod
    def from_dict(cls, json_dict):
        try:
            return cls(**json_dict)
        except TypeError:
            raise ValueError(
                '"{json_dict}" is NOT a valid zhuge token json.'.format(
                    json_dict=json_dict
                ))

    @classmethod
    def to_dict(cls):
        return cls.__dict__


class ZhugeClient:
    def __init__(self, token_file=TOKEN_FILE):
        self.token_file = token_file
        self._session = requests.session()
        self.login()

    def save_token(self, data):
        res = self._session.post(LOGIN_URL, data=data)
        try:
            json_dict = res.json()
            if 'error' in json_dict:
                raise LoginException(json_dict['error']['message'])
            self._token = ZhugeToken.from_dict(json_dict)
        except (ValueError, KeyError) as e:
            raise LoginException(str(e))
        else:
            ZhugeToken.save_file(self.token_file, json_dict['user'])

    def login(self):

        json_data = {"username": os.environ.get("username"),
                     "password": os.environ.get("password"),
                     "type": 0, "location": ""}
        data = {"data": json.dumps(json_data)}
        self.save_token(data)


if __name__ == '__main__':
    client = ZhugeClient()
