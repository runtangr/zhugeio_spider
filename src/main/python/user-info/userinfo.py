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
    cookies = dict(JSESSIONID="EDDAFF6BB1D9AAA5916F81599BEC855D.gw1")
    result = requests.get(url,cookies=cookies)
    print (result.text)

def find(page):
    url = 'https://zhugeio.com/appuser/find.jsp'
    cookies = dict(JSESSIONID="EDDAFF6BB1D9AAA5916F81599BEC855D.gw1")
    data = {
            "appId":48971,
            "platform":2,
            "json":"[]",
            "page":1,
            "rows":20,
            "total":0,
            "order_by":"last_visit_time"
            }
    result = requests.post(url,cookies=cookies,data=data)
    # print (result.text)
    return result.text

def getUserid():
    g = (x for x in range(1,1000))
    for page in g:
        results = find(page)
        datas = json.loads(results)
        if "login" in datas["values"] and datas["values"]["login"]==False:
            print(results)
            break
        if len(datas["values"]["users"]) == 0:
            break
        it = iter(datas["values"]["users"])
        while True:
            try:
                # 获得下一个值:
                data = next(it)
                yield data["zg_id"]
            except StopIteration:
                # 遇到StopIteration就退出循环
                break
    return

if __name__ == "__main__":
    currentUser()
    for userid in getUserid():
        print(userid)


   

        




