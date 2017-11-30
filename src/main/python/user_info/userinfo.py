# -*- coding:utf-8 -*-

import json
import requests
import datetime
import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(basedir)

from analog_login import login

'''
    function: get data from zhugeio and save data to json file.
'''


class UserInfo(object):

    def __init__(self):
        # exe_mode: "000000"
        #              |||| status 0: not deal, 1: write base data.
        #              ||| status 0: not deal, 1: write UserInfos data.
        #              || status 0: not deal, 1: write Yesterday's Sessions data.
        #              | status 0: not deal, 1: write all Sessions data.
        # plat_form: 1 or 2 or 3  1:android 2:ios 3:pc
        # user_type 0 or 1  0:All user 1:Real user

        self.user_type = 1

        self.plat = {
            1: "Android",
            2: "Ios",
            3: "PC"
        }
        self.plat_form = 3
        if self.plat_form == 3:
            self.app_id = 54453
        else:
            self.app_id = 48971
        self.exe_mode = "000100"
        self.cookies = login.login()

    def current_user(self):
        url = 'https://zhugeio.com/company/currentUser.jsp'
        result = requests.get(url, cookies=self.cookies)
        print(result.text)

    def find_base(self, page):
        # description: find all user base data.
        #
        # page: 0~
        # platform: 1 or 2  1:Android 2:ios

        url = 'https://zhugeio.com/appuser/find.jsp'
        data = {
                "appId": self.app_id,
                "platform": self.plat_form,
                "json": "[]",
                "page": page,
                "rows": 20,
                "total": 0,
                "order_by": "last_visit_time"
                }
        result = requests.post(url, cookies=self.cookies, data=data)
        # print (result.text)
        return result.text

    def get_user_info(self, search_base_data):
        # description: get all user_id.

        first_visit_time = ""
        app_user_id = ""
        it = iter(search_base_data["values"]["users"])
        for search_user_info in it:
            for fixed_property in search_user_info["fixed_properties"]:

                if fixed_property["property_name"] == "first_visit_time":
                    first_visit_time = fixed_property["property_value"]
                if fixed_property["property_name"] == "app_user_id":
                    app_user_id = fixed_property["property_value"]
            # get real user.
            if self.user_type == 1 and app_user_id is not None:

                yield (search_user_info["zg_id"],
                       first_visit_time)

        return

    def manage_data(self):
        # mange user data by find module. multitask
        # deal data by different mode.
        # exec_mode: "000000"
        #                ||| status 0: not deal, 1: write base data.
        #                || status 0: not deal, 1: write UserInfo data.
        #                | status 0: not deal, 1: write Sessions data.

        g = range(1, 1000)
        for page in g:
            results = self.find_base(page)
            base_data = json.loads(results, encoding="utf-8")

            if ("login" in base_data["values"] and
                    base_data["values"]["login"] is False):
                print(results)
                break
            if len(base_data["values"]["users"]) == 0:
                break

            if self.exe_mode[-1] == "1":
                yield base_data

            if (self.exe_mode[-2] == "1"
                    or self.exe_mode[-3] == "1"
                    or self.exe_mode[-4] == "1"):
                yield self.get_user_info(base_data)

            if self.exe_mode[-5] == "1":
                pass

    @staticmethod
    def build_base_data(user_datas):

        for name, value in user_datas.items():
            if name != "zg_id":
                for data in value:
                    yield data["property_name"], data["property_value"]

        return "done"

    @staticmethod
    def build_user_info_data(user_data):

        for data in user_data["app_data"]["user"]["app_user"]:
            yield data["name"], data["value"]

        return "done"

    @staticmethod
    def build_sessions_data(user_data):

        for sessionInfo in user_data["values"]["sessionInfos"]:
            yield sessionInfo

        return "done"

    @staticmethod
    def get_user_data(users):
        for data in users["values"]["users"]:
            yield data

        return

    def write_user_data2file(self, datas,
                             data_type, begin_day_id=None):
        # write user base data to ****.dat .

        if data_type == "Session":
            if self.exe_mode == "001000":
                with open('./user_file/{data_type}{platform}_all.json'.format(
                        data_type=data_type,
                        platform=self.plat[self.plat_form]),
                        'a') as f:
                    f.writelines(json.dumps(datas, ensure_ascii=False) + '\n')
            else:
                with open('./user_file/{data_type}{platform}_{beginDayId}.json'.format(
                        data_type=data_type,
                        platform=self.plat[self.plat_form],
                        beginDayId=begin_day_id),
                          'a') as f:
                    f.writelines(json.dumps(datas, ensure_ascii=False) + '\n')
        else:
            with open('./user_file/{data_type}{platform}.json'.format(
                    data_type=data_type,
                    platform=self.plat[self.plat_form]),
                      'a') as f:
                f.writelines(json.dumps(datas, ensure_ascii=False) + '\n')

    def find_user_info(self, uid):
        # description: find all user UserInfo data.
        # uid: user id
        # platform: 1 or 2  1:Android 2:ios

        result = self.query_user_info(uid)
        # print (result)
        return result

    def query_user_info(self, uid):

        url = 'https://zhugeio.com/appuser/queryUserInfos.jsp'
        data = {
            "appId": self.app_id,
            "platform": self.plat_form,
            "uid": uid
        }
        result = requests.post(url, cookies=self.cookies, data=data)
        # print (result.text)
        return result.text

    def sessions(self, uid, begin_day_id):
        url = 'https://zhugeio.com/appuser/sessions.jsp'
        data = {
            "appId": self.app_id,
            "platform": self.plat_form,
            "uid": uid,
            "beginDayId": begin_day_id
        }
        result = requests.post(url, cookies=self.cookies, data=data)
        # print (result.text)
        return result.text

    def sessions_attr_info(self, uid,
                           event_id, session_id,
                           uuid, begin_date):
        url = 'https://zhugeio.com/appuser/querySessionAttrInfos.jsp'
        data = {
            "appId": self.app_id,
            "platform": self.plat_form,
            "uid": uid,
            "eventId": event_id,
            "sessionId": session_id,
            "uuid": uuid,
            "beginDate": begin_date
        }
        result = requests.post(url, cookies=self.cookies, data=data)
        # print (result.text)
        return result.text

    def get_user_id(self):
        for user_id_generator in self.manage_data():
                for user_id, first_visit_time in user_id_generator:
                    yield user_id

    def get_user_infos_data(self, user_id):
        # deal data by UserInfo mode.

        app_user = {}

        result = self.find_user_info(user_id)
        result_js = json.loads(result)

        for name, value in self.build_user_info_data(result_js):
            app_user[name] = value

        return result_js, app_user, result_js["app_data"]["user"]["sessionDays"]

    def write_user_infos_data(self):
        # deal data by UserInfos mode.
        for search_user_id in self.get_user_id():
            result_js, app_user, _ = self.get_user_infos_data(search_user_id)

            result_js["app_data"]["user"]["app_user"] = app_user

            self.write_user_data2file(result_js, data_type="UserInfos")

    def write_base_data(self):
        build_data = {}
        for datas in self.manage_data():
            for user_data in self.get_user_data(datas):
                build_data["zg_id"] = user_data["zg_id"]
                for k, v in self.build_base_data(user_data):
                    build_data[k] = v
                self.write_user_data2file(build_data, data_type="Base")

    def get_session_info(self, user_id, session_info):
        if len(session_info["events"]) == 0:
            return ""
        ip = ""
        column_code = ""
        for index, event in enumerate(session_info["events"]):

            result = self.sessions_attr_info(user_id,
                                             event["eventId"],
                                             session_info["sessionId"],
                                             event["uuid"],
                                             event["beginDate"])

            result_json = json.loads(result)

            for env_info in result_json["app_data"][0]["env_infos"]:
                if env_info["name"] == "ip":
                    ip = env_info["value"]
                    break

            for attr_info in result_json["app_data"][0]["attr_infos"]:
                if attr_info["attrName"] == "columnCode":
                    column_code = attr_info["eventValue"]
                    break

            event["ip"] = ip
            event["column_code"] = column_code
            yield index, event

    def write_sessions_yest_data(self, begin_day_id=None):
        # deal data by sessions mode.

        for user_id in self.get_user_id():
            result = self.sessions(user_id, begin_day_id)
            result_js = json.loads(result)

            for sessionInfo in self.build_sessions_data(result_js):
                sessionInfo["zg_id"] = user_id
                sessionInfo["beginDayId"] = begin_day_id

                for index, event in self.get_session_info(user_id, sessionInfo):
                    sessionInfo["events"][index] = event

                self.write_user_data2file(
                                     sessionInfo,
                                     data_type="Session",
                                     begin_day_id=begin_day_id)

    def write_sessions_all_data(self):
        # deal data by sessions mode.

        for user_id in self.get_user_id():

            # get this user dayId
            for begin_day_id in self.get_day_id(user_id):
                # get session data by user_id and beginDayId.
                result = self.sessions(user_id, begin_day_id)
                result_js = json.loads(result)
                for sessionInfo in self.build_sessions_data(result_js):
                    sessionInfo["zg_id"] = user_id
                    sessionInfo["beginDayId"] = begin_day_id
                    sessionInfo["events"] = []

                    for event in self.get_session_info(user_id, sessionInfo):
                        sessionInfo["events"].append(event)
                    self.write_user_data2file(
                                         sessionInfo,
                                         data_type="Session",
                                         begin_day_id=begin_day_id)

    def get_day_id(self, user_id):
        _, _, session_days = self.get_user_infos_data(user_id)
        for sessionDay in session_days:
            if sessionDay["numbers"] != 0:
                yield sessionDay["dayId"]

    def deal_data(self):
        if self.exe_mode[-1] is "1":
            self.write_base_data()

        if self.exe_mode[-2] is "1":
            self.write_user_infos_data()

        if self.exe_mode[-3] is "1":
            yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

            begin_day_id = int(yesterday.strftime("%Y%m%d"))
            self.write_sessions_yest_data(begin_day_id)

        if self.exe_mode[-4] is "1":

            self.write_sessions_all_data()

if __name__ == "__main__":

    user_info = UserInfo()

    user_info.current_user()

    user_info.deal_data()
