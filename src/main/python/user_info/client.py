# -*- coding:utf-8 -*-

import requests
import json
import time
import os
from requests.auth import AuthBase
from exception import LoginException
from config import LOGIN_URL, TOKEN_FILE, CLIENT_ID

'''
user login and save token.
'''


class ZhugeOAuth(AuthBase):
    def __init__(self, token=None):
        self._token = token

    def __call__(self, r):
        if self._token is None:
            auth_str = '{client_id}'.format(
                client_id=self._token
            )
        else:
            auth_str = '{token}'.format(

                token=str(self._token)
            )
        r.headers['Authorization'] = auth_str
        return r


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
        if os.path.exists(token_file):
            # self._token = ZhugeToken.from_file(token_file)
            self.login()
        else:
            self.login()
        self.auth = ZhugeOAuth(self._token)

    def save_token(self, auth, data):
        res = self._session.post(LOGIN_URL, auth=ZhugeOAuth(), data=data)
        try:
            json_dict = res.json()
            if 'error' in json_dict:
                raise LoginException(json_dict['error']['message'])
            self._token = ZhugeToken.from_dict(json_dict)
        except (ValueError, KeyError) as e:
            # login again
            time.sleep(5)
            self.save_token(auth, data)

        # else:
            # ZhugeToken.save_file(self.token_file, json_dict)

    def login(self):
        self.login_auth = ZhugeOAuth()
        json_data = {"username": os.getenv("USER_NAME"),
                     "password": os.getenv("PASSWORD"),
                     "type": 0, "location": ""}
        data = {"data": json.dumps(json_data)}
        self.save_token(self.login_auth, data)


if __name__ == '__main__':
    client = ZhugeClient()
