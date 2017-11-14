# -*- coding:utf-8 -*-

import json
import requests
import datetime

def currentUser():
    url = 'https://zhugeio.com/company/currentUser.jsp'
    header = {
        "Accept": "application/json, text/javascript, */*; q=0.01",

        "Host": "zhugeio.com",

        "Origin": "https://zhugeio.com",
    
       "Referer": "https://zhugeio.com/appuser/toPage.jsp?app_id=48971&p=2",
    
        "User-Agent":"Mozilla/5.0(Windows NT6.1;WOW64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/61.0.3163.100Safari/537.36"
    }
    cookies = dict(JSESSIONID="ED65CB5B7B13891BC9F51E9B11CF7FEB.gw1")
    result = requests.get(url,cookies=cookies)
    print (result.text)

def find():
    url = 'https://zhugeio.com/appuser/find.jsp'
    cookies = dict(JSESSIONID="ED65CB5B7B13891BC9F51E9B11CF7FEB.gw1")
    # data = "appId=48971&platform=2&json=%5B%5D&page=1&rows=20&total=0&order_by=last_visit_time%2Cdesc"
    # last_visit_time = datetime.datetime.now()
    data = {
            "appId":"48971",
            "platform":"2",
            "json":"[]",
            "page":"1",
            "rows":"20",
            "total":"0"
            }
    
    # "order_by":"last_visit_time,desc"
    result = requests.post(url,cookies=cookies,data=data)
    print (result.text)
    return result.text

if __name__ == "__main__":
   result = find()

