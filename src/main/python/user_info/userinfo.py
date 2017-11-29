# -*- coding:utf-8 -*-
#!/usr/bin/env python3
import json
import requests
import datetime
import os
import sys
from analog_login import login
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(basedir)
cookies = login.login()


def current_user():
    '''
    description: set current user by cookie.
    '''
    url = 'https://zhugeio.com/company/currentUser.jsp'
    result = requests.get(url, cookies=cookies)
    print(result.text)


def find_base(page, platform):
    '''
    description: find all user base data.
    page: 0~ 
    platform: 1 or 2  1:Android 2:ios
    '''
    url = 'https://zhugeio.com/appuser/find.jsp'
    data = {
            "appId": 48971,
            "platform": platform,
            "json": "[]",
            "page": page,
            "rows": 20,
            "total": 0,
            "order_by": "last_visit_time"
            }
    result = requests.post(url, cookies=cookies, data=data)
    # print (result.text)
    return result.text


def get_userinfos(datas):
    '''
    description: get all userid.
    '''

    it = iter(datas["values"]["users"])
    for userinfo in it:
        for fixed_propert in userinfo["fixed_properties"]:
            if fixed_propert["property_name"] == "first_visit_time":
                yield userinfo["zg_id"], fixed_propert["property_value"]

    return

def manageData(platform, exec_mode="000001"):
    '''
    mange user data by find module. multitask
    deal data by different mode.
    exec_mode: "000000"
                   ||| status 0: not deal, 1: write base data. 
                   || status 0: not deal, 1: write UserInfos data.
                   | status 0: not deal, 1: write Sessions data.
                    
    '''
    #python3 range is generator
    g = range(1, 1000)
    for page in g:
        results = find_base(page, platform)
        datas = json.loads(results, encoding="utf-8")

        if "login" in datas["values"] and datas["values"]["login"] == False:
            print(results)
            break
        if len(datas["values"]["users"]) == 0:
            break

        if exec_mode[-1] == "1":
            yield datas

        if exec_mode[-2] == "1" or exec_mode[-3] == "1" \
                or exec_mode[-4] == "1":
            yield get_userinfos(datas)

        if exec_mode[-5] == "1":
            pass

def buildBaseData(user_datas):

    for name,value in user_datas.items():
        if name!="zg_id":
            for data in value:
                yield data["property_name"], data["property_value"]

    return "done"

def buildUserInfosData(user_data):

    for data in user_data["app_data"]["user"]["app_user"]:
        yield data["name"],data["value"]

    return "done"

def buildSessionsData(user_data):

    for sessionInfo in user_data["values"]["sessionInfos"]:
        yield sessionInfo

    return "done"

def getUserData(datas):
    it = iter(datas["values"]["users"])
    while True:
        try:
            data = next(it)
            yield data
        except StopIteration:
            break
    return

def writeUserData2File(platform, datas,
                       data_type, begin_day_id=None,
                       exe_mode=None):
    '''
    write user base data to ****.dat .
    '''
    if data_type=="Session":
        if exec_mode == "001000":
            with open('./user_file/{data_type}{platform}_all.json'.format(
                    data_type=data_type,
                    platform=("Ios" if platform > 1 else "Android")),
                      'a') as f:
                f.writelines(json.dumps(datas, ensure_ascii=False) + '\n')
        else:
            with open('./user_file/{data_type}{platform}_{beginDayId}.json'.format(
                    data_type=data_type,
                    platform=("Ios" if platform > 1 else "Android"),
                    beginDayId=begin_day_id),
                      'a') as f:
                f.writelines(json.dumps(datas, ensure_ascii=False) + '\n')
    else:
        with open('./user_file/{data_type}{platform}.json'.format(
                data_type=data_type,
                platform=("Ios" if platform > 1 else "Android")),
                  'a') as f:
            f.writelines(json.dumps(datas, ensure_ascii=False) +'\n')


def findUserInfos(platform, uid):
    '''
    description: find all user UserInfos data.
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


def sessions(platform, uid, begin_day_id):
    url = 'https://zhugeio.com/appuser/sessions.jsp'
    data = {
        "appId": 48971,
        "platform": platform,
        "uid": uid,
        "beginDayId": begin_day_id
    }
    result = requests.post(url, cookies=cookies, data=data)
    # print (result.text)
    return result.text


def sessions_attr_info(plat_form, uid, event_id, session_id, uuid, begin_date):
    url = 'https://zhugeio.com/appuser/querySessionAttrInfos.jsp'
    data = {
        "appId": 48971,
        "platform": plat_form,
        "uid": uid,
        "eventId": event_id,
        "sessionId": session_id,
        "uuid": uuid,
        "beginDate": begin_date
    }
    result = requests.post(url, cookies=cookies, data=data)
    # print (result.text)
    return result.text

def getUserId(platform, exec_mode):
    for userid_generator in manageData(platform, exec_mode=exec_mode):
            for userid, first_visit_time in userid_generator:
                yield userid

def getUserInfosData(platform, exec_mode, userid):
    '''
    deal data by UserInfos mode.                
    '''
    # write UserInfos data.
    app_user = {}

    result = findUserInfos(platform, userid)
    result_js = json.loads(result)

    for name,value in buildUserInfosData(result_js):
        app_user[name] = value

    return result_js, app_user, result_js["app_data"]["user"]["sessionDays"]

def writeUserInfosData(platform,exec_mode):
    '''
    deal data by UserInfos mode.                
    '''
    # write UserInfos data.
    for userid in getUserId(platform,exec_mode):
        result_js, app_user, _ = getUserInfosData(platform,exec_mode, userid)

        result_js["app_data"]["user"]["app_user"] = app_user

        writeUserData2File(platform, result_js,data_type="UserInfos")

def writeBaseData(platform, exec_mode):
    build_data = {}
    for datas in manageData(platform, exec_mode=exec_mode):
        for user_data in getUserData(datas):
            build_data["zg_id"] = user_data["zg_id"]
            for k, v in buildBaseData(user_data):
                build_data[k] = v
            writeUserData2File(platform, build_data, data_type="Base")


def get_session_ip(plat_form, user_id, session_info):
    if len(session_info["events"]) == 0:
        return ""
    uuid = session_info["events"][0]["uuid"]
    begin_date = session_info["events"][0]["beginDate"]
    event_id = session_info["events"][0]["eventId"]

    session_id = session_info["sessionId"]

    result = sessions_attr_info(plat_form, user_id, event_id, session_id, uuid, begin_date)

    result_json = json.loads(result)
    for env_info in result_json["app_data"][0]["env_infos"]:
        if env_info["name"] == "ip":
            return env_info["value"]


def writeUserSessionsYestData(platform, exec_mode, beginDayId=None):
    '''
        deal data by sessions mode.                
        '''
    # write sessions data.
    for userid in getUserId(platform, exec_mode):
        result = sessions(platform, userid, beginDayId)
        result_js = json.loads(result)

        for sessionInfo in buildSessionsData(result_js):
            sessionInfo["zg_id"] = userid
            sessionInfo["beginDayId"] = beginDayId
            sessionInfo["ip"] = get_session_ip(platform, userid, sessionInfo)
            writeUserData2File(platform,
                               sessionInfo,
                               data_type="Session",
                               begin_day_id=beginDayId,
                               exe_mode=exec_mode)

def writeUserSessionsAllData(platform, exec_mode, beginDayId=None):
    '''
        deal data by sessions mode.                
        '''
    # write sessions data.
    for userid in getUserId(platform, exec_mode):

        # get this user dayId
        for beginDayId in getDayid(platform, exec_mode,userid):
            #get session data by userid and beginDayId.
            result = sessions(platform, userid, beginDayId)
            result_js = json.loads(result)
            for sessionInfo in buildSessionsData(result_js):
                sessionInfo["zg_id"] = userid
                sessionInfo["beginDayId"] = beginDayId
                writeUserData2File(platform,
                                   sessionInfo,
                                   data_type="Session",
                                   begin_day_id=beginDayId,
                                   exe_mode=exec_mode)

def getDayid(platform, exec_mode, user_id):
    _, _, sessionDays = getUserInfosData(platform, exec_mode, user_id)
    for sessionDay in sessionDays:
        if sessionDay["numbers"] != 0:
            yield sessionDay["dayId"]

def dealData(platform,exec_mode):
    if exec_mode[-1] is "1":
        writeBaseData(platform, exec_mode)

    if exec_mode[-2] is "1":
        writeUserInfosData(platform, exec_mode)

    if exec_mode[-3] is "1":
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

        begin_day_id = int(yesterday.strftime("%Y%m%d"))
        writeUserSessionsYestData(platform, exec_mode, begin_day_id)

    if exec_mode[-4] is "1":

        writeUserSessionsAllData(platform, exec_mode)

if __name__ == "__main__":
    '''
      exec_mode: "000000"
                    |||| status 0: not deal, 1: write base data. 
                    ||| status 0: not deal, 1: write UserInfos data.
                    || status 0: not deal, 1: write Yesterday's Sessions data.
                    | status 0: not deal, 1: write all Sessions data.
      platform: 1 or 2  1:Android 2:ios
      '''
    platform = 2

    current_user()

    exec_mode = "000100"
    dealData(platform, exec_mode)


   

        




