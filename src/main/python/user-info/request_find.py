# -*- coding:utf-8 -*-

import json
import requests

def request_find():
    url = "https://zhugeio.com/appuser/find.jsp"
    header = {
        "Accept": "* / *",

        "Host": "zhugeio.com",

        "Origin": "https: // zhugeio.com",

        "Referer": "https: // zhugeio.com / appuser / toPage.jsp?app_id = 48971 & p = 2",

        "User - Agent": "Mozilla / 5.0(Windows NT 6.1; WOW64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/63.0.3236.0 Safari/537.36"
    }
    result = requests.post(url)
    print result.text

if __name__ == "__main__":
    request_find()