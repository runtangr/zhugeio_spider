# -*- coding:utf-8 -*-

import json
import requests
import datetime
import os
import sys
from client import ZhugeClient, ZhugeToken
from config import (
    CURRENT_USER, FIND_URL, USER_INFO_URL, SESSION_URL,
    SESSION_ATTR_INFO_URL, INFO_TYPE, ALL_SESSION_PATH,
    YEST_SESSION_PATH, INFO_PATH, BASE_PATH, PLATFORM,
    INFO_DIR, TOKEN_FILE, APP_INFO)

'''
    function: get data from zhugeio and save data to json file.
'''


class UserInfo(ZhugeClient):

    def __init__(self):
        # exe_mode: "000000"
        #              |||| status 0: not deal, 1: write base data.
        #              ||| status 0: not deal, 1: write UserInfos data.
        #              || status 0: not deal, 1: write Yesterday's Sessions data.
        #              | status 0: not deal, 1: write all Sessions data.
        # platform: 1 or 2 or 3  1:android 2:ios 3:pc
        # user_type 0 or 1  0:All user 1:Real user

        super(UserInfo, self).__init__()

        self.user_type = 1

        self.platform = 3
        self.platform_content = PLATFORM[self.platform]

        self.app_id = self.get_app_id()

        self.exe_mode = "000100"

        self.client = ZhugeClient()

    def current_user(self):

        result = self._session.get(CURRENT_USER)
        print(result.text)

    def get_app_id(self):
        res = self._session.get(APP_INFO)
        res_dict = res.json()
        app_id = res_dict['applist'][0]['id']

        return app_id

    def query_user_info(self, uid):

        data = {
            "appId": self.app_id,
            "platform": self.platform,
            "uid": uid
        }
        result = self._session.post(USER_INFO_URL, data=data)
        # print (result.text)
        return result

    def sessions(self, uid, begin_day_id):
        data = {
            "appId": self.app_id,
            "platform": self.platform,
            "uid": uid,
            "beginDayId": begin_day_id
        }
        result = self._session.post(SESSION_URL, data=data)
        # print (result.text)
        return result

    def sessions_attr_info(self, uid,
                           event_id, session_id,
                           uuid, begin_date):
        data = {
            "appId": self.app_id,
            "platform": self.platform,
            "uid": uid,
            "eventId": event_id,
            "sessionId": session_id,
            "uuid": uuid,
            "beginDate": begin_date
        }
        result = self._session.post(SESSION_ATTR_INFO_URL, data=data)
        # print (result.text)
        return result

    def find_base(self, page):
        # description: find all user base data.
        #
        # page: 0~
        # platform: 1 or 2  1:Android 2:ios

        data = {
                "appId": self.app_id,
                "platform": self.platform,
                "json": "[]",
                "page": page,
                "rows": 20,
                "total": 0,
                "order_by": "last_visit_time"
                }
        result = self._session.post(FIND_URL, data=data)
        # print (result.text)
        return result

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
            elif self.user_type != 1:
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
            # base_data = json.loads(results, encoding="utf-8")
            base_data = results.json()

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

    @staticmethod
    def save_file(path, data):

        with open(path, 'a') as f:
            f.writelines(''.join([json.dumps(data, ensure_ascii=False), '\n']))

    def write_user_data2file(self, datas,
                             data_type, begin_day_id=None):
        # write user base data to ****.dat .

        if not os.path.exists(INFO_DIR):
            os.makedirs(INFO_DIR)
        if data_type == "Session":
            if self.exe_mode == "001000":
                session_path = ALL_SESSION_PATH.format(self.platform_content)
                self.save_file(session_path, datas)
            else:
                yest_session_path = YEST_SESSION_PATH.format(platform=self.platform_content,
                                                             begin_day_id=begin_day_id)
                self.save_file(yest_session_path, datas)
        elif data_type == "Infos":
            info_path = INFO_PATH.format(self.platform_content)
            self.save_file(info_path, datas)

        elif data_type == "Base":
            base_path = BASE_PATH.format(self.platform_content)
            self.save_file(base_path, datas)

    def find_user_info(self, uid):
        # description: find all user UserInfo data.
        # uid: user id
        # platform: 1 or 2  1:Android 2:ios

        result = self.query_user_info(uid)
        # print (result)
        return result

    def get_user_id(self):
        for user_id_generator in self.manage_data():
                for user_id, first_visit_time in user_id_generator:
                    yield user_id

    def get_user_infos_data(self, user_id):
        # deal data by UserInfo mode.

        app_user = {}

        result = self.find_user_info(user_id)
        result_js = result.json()

        for name, value in self.build_user_info_data(result_js):
            app_user[name] = value

        return result_js, app_user, result_js["app_data"]["user"]["sessionDays"]

    def write_user_infos_data(self):
        # deal data by UserInfos mode.
        for search_user_id in self.get_user_id():
            result_js, app_user, _ = self.get_user_infos_data(search_user_id)

            result_js["app_data"]["user"]["app_user"] = app_user

            self.write_user_data2file(result_js, data_type="Infos")

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

            result_json = result.json()

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
            result_js = result.json()

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
                result_js = result.json()
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
