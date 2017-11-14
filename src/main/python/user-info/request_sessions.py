# -*- coding:utf-8 -*-

import json
import requests

def request_sessions():
    url = 'https://zhugeio.com/appuser/sessions.jsp'
    header = {
        "Accept": "application/json, text/javascript, */*; q=0.01",

        "Host": "https://zhugeio.com",

        "Origin": "https://zhugeio.com",
    
       "Referer": "https://zhugeio.com/appuser/toPage.jsp?app_id=48971&p=2",
    
        "User-Agent": "Mozilla/5.0(Windows NT6.1; WOW64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/61.0.3163.100Safari/537.36"
    }
    result = requests.get(url,headers=header)
    print (result.text)

if __name__ == "__main__":
    request_sessions()