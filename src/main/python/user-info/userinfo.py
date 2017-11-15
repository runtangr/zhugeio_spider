# -*- coding:utf-8 -*-

import json
import requests
import datetime

cookies = dict(JSESSIONID="FD2FBE5C1915137E9CE79B2E184A211D.gw1")
g = (x for x in range(1, 1000))

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

def getUserid(datas):
    '''
    description: get all userid.
    '''

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

def manage_data(platform, exec_mode="000001"):
    '''
    mange user data by find module. multitask
    :param platform:  1 or 2  1:Android 2:ios
    :param exec_mode: can select one or more mode
    :return: 
    '''
    for page in g:
        results = find(page, platform)
        datas = json.loads(results)

        if "login" in datas["values"] and datas["values"]["login"] == False:
            print(results)
            break
        if len(datas["values"]["users"]) == 0:
            break

        if exec_mode[-1] == "1":
            yield getUserid(datas)

        if exec_mode[-2] == "1":
            pass

        if exec_mode[-3] == "1":
            pass

        if exec_mode[-4] == "1":
            pass

        if exec_mode[-5] == "1":
            pass



def writeBase(platform):
    '''
    write user base data to userbase.dat .
    platform: 1 or 2  1:Android 2:ios
    '''
    for page in g:
        results = find(page,platform)
        datas = json.loads(results)

        if "login" in datas["values"] and datas["values"]["login"]==False:
            print(results)
            break
        if len(datas["values"]["users"]) == 0:
            break

        with open('./user-file/userBase.dat', 'ab') as f:
            print(f.write(datas))


if __name__ == "__main__":
    platform = 2
    page = 2
    currentUser()
    # find(page,platform)

    # for userid in getUserid(platform):
    #     print(userid)

    # writeBase(platform)

    for userid_generator in manage_data(platform, exec_mode="000011"):
        print (userid_generator)
        for userid in userid_generator:
            print (userid)

   

        




