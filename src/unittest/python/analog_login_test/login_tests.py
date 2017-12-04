#encoding=utf-8
#!/usr/bin/env python3
__author__ = 'tangr'

import unittest
import requests
from analog_login import login


class Client(unittest.TestCase):

    def test_login(self):
        cookie = login.login()
        url = 'https://zhugeio.com/company/currentUser.jsp'
        result = requests.get(url, cookies=cookie)
        print(result.text)
