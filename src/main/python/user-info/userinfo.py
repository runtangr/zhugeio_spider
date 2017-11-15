# -*- coding:utf-8 -*-

import json
import requests
import datetime

cookies = dict(JSESSIONID="FD2FBE5C1915137E9CE79B2E184A211D.gw1")

def currentUser():
    '''
    description: set current user by cookie.
    '''
    url = 'https://zhugeio.com/company/currentUser.jsp'
    result = requests.get(url,cookies=cookies)
    # print (result.text)

def findBase(page,platform):
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

def manageData(platform, exec_mode="000001"):
    '''
    mange user data by find module. multitask
    :param platform:  1 or 2  1:Android 2:ios
    :param exec_mode: can select one or more mode
    :return: 
    '''
    g = (x for x in range(1, 1000))
    for page in g:
        results = findBase(page, platform)
        datas = json.loads(results)

        if "login" in datas["values"] and datas["values"]["login"] == False:
            print(results)
            break
        if len(datas["values"]["users"]) == 0:
            break

        if exec_mode[-1] == "1":
            yield getUserid(datas)

        if exec_mode[-2] == "1":
            writeBase(platform,datas)

        if exec_mode[-3] == "1":
            pass

        if exec_mode[-4] == "1":
            pass

        if exec_mode[-5] == "1":
            pass

def writeBase(platform,datas):
    '''
    write user base data to userbase.dat .
    '''

    with open('./user-file/userBase%s.dat' % ("Ios" if platform>1 else "Android") , 'ab') as f:
        f.write(str(datas))

def writeDetail(platform,datas):
    '''
    write user base data to userDetail.dat .
    '''

    with open('./user-file/userDetail%s.dat' % ("Ios" if platform>1 else "Android") , 'ab') as f:
        f.write(str(datas))


def findDetail(platform,uid):
    '''
    description: find all user detail data.
    uid: user id  
    platform: 1 or 2  1:Android 2:ios
    '''
    result = queryUserInfos(platform, uid)
    # print (result)
    return result

def queryUserInfos(platform, uid):

    url = 'https://zhugeio.com/appuser/queryUserInfos.jsp'
    data = {
        "appId": 48971,
        "platform": platform,
        "uid": uid
    }
    result = requests.post(url, cookies=cookies, data=data)
    # print (result.text)
    return result.text


def sessions(platform, uid):
    url = 'https://zhugeio.com/appuser/sessions.jsp'
    data = {
        "appId": 48971,
        "platform": platform,
        "uid": uid,
        "beginDayId": "20171114"
    }
    result = requests.post(url, cookies=cookies, data=data)
    # print (result.text)
    return result.text

if __name__ == "__main__":
    platform = 1
    # page = 2
    exec_mode = "000001"
    currentUser()
    # find(page,platform)

    # for userid in getUserid(platform):
    #     print(userid)

    # writeBase(platform)

    for userid_generator in manageData(platform, exec_mode=exec_mode):
        for userid in userid_generator:
            print (userid)
            result = findDetail(platform,userid)
            result_js = json.loads(result)
            writeDetail(platform,result_js)

   

        




