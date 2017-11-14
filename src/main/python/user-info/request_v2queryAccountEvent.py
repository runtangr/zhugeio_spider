# -*- coding:utf-8 -*-

import json
import requests

def request_v2queryAccountEvent():
    url = "https://zhugeio.com/contract/v2queryAccountEvent.jsp"
    header = {
        "Accept": "*/*",

        "Host": "zhugeio.com",

        "Origin": "https: // zhugeio.com",

        "Referer": "https: // zhugeio.com / data / eventAnalysis.jsp?app_id = 48971",

        "User - Agent": "Mozilla / 5.0(Windows NT 6.1; WOW64) AppleWebKit / 537.36 (KHTML, likeGecko) Chrome / 63.0.3236.0Safari / 537.36"
    }
    result = requests.post(url,headers = header)
    print result.text

if __name__ == "__main__":
    request_v2queryAccountEvent()