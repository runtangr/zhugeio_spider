# -*- coding:utf-8 -*-

import json
import requests
import datetime

cookies = dict(JSESSIONID="0DFCE1E49455D77F052F2B6191DBAA87.gw1")

def currentUser():
    '''
    description: set current user by cookie.
    '''
    url = 'https://zhugeio.com/company/currentUser.jsp'
    result = requests.get(url,cookies=cookies)
    # print (result.text)

def find(page,platform):
    '''
    description: find all user base data.
    page: 0~ 
    platform: 1 or 2  1:Android 2:ios
    '''
    url = 'https://zhugeio.com/appuser/find.jsp'
    data = {
            "appId":48971,
            "platform":platform,
            "json":"[]",
            "page":page,
            "rows":20,
            "total":0,
            "order_by":"last_visit_time"
            }
    result = requests.post(url,cookies=cookies,data=data)
    # print (result.text)
    return result.text

def getUserid(platform):
    '''
    description: get all userid.
    platform: 1 or 2  1:Android 2:ios
    '''
    g = (x for x in range(1,1000))
    for page in g:
        results = find(page,platform)
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

def writeBase(platform):
    '''
    write user base data to userbase.dat .
    platform: 1 or 2  1:Android 2:ios
    '''
    g = (x for x in range(1, 1000))
    for page in g:
        results = find(page,platform)
        datas = json.loads(results)
        if "login" in datas["values"] and datas["values"]["login"]==False:
            print(results)
            break
        if len(datas["values"]["users"]) == 0:
            break


if __name__ == "__main__":
    platform = 2
    page = 2
    currentUser()
    # find(page,platform)
    for userid in getUserid(platform):
        print(userid)


   

        




