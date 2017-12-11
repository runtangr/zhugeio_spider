# -*- coding:utf-8 -*-

import json
import datetime
import os
import asyncio
import aiohttp
import math
from client import ZhugeClient, ZhugeToken
from config import (
    CURRENT_USER, FIND_URL, USER_INFO_URL, SESSION_URL,
    SESSION_ATTR_INFO_URL, INFO_TYPE, ALL_SESSION_PATH,
    YEST_SESSION_PATH, INFO_PATH, BASE_PATH, PLATFORM,
    INFO_DIR, TOKEN_FILE, APP_INFO, USER_NUM)

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
        self.exe_mode = "000111"

        self.headers = {}

        self.client = ZhugeClient()

        self.app_id = self.get_app_id()

    def current_user(self):

        result = self._session.get(CURRENT_USER)
        print(result.text)

    def get_app_id(self):
        res = self._session.get(APP_INFO, headers=self.headers, auth=self.auth)
        res_dict = res.json()
        app_id = res_dict['applist'][0]['id']

        return app_id

    async def query_user_info(self, uid):

        data = {
            "appId": self.app_id,
            "platform": self.platform,
            "uid": uid
        }
        async with aiohttp.ClientSession(cookies=self._session.cookies) as session:
            async with session.post(url=USER_INFO_URL, data=data) as resp:
                rs = await resp.json()
        # print (result.text)
        return rs

    async def sessions(self, uid, begin_day_id):
        data = {
            "appId": self.app_id,
            "platform": self.platform,
            "uid": uid,
            "beginDayId": begin_day_id
        }
        async with aiohttp.ClientSession(cookies=self._session.cookies) as session:
            async with session.post(url=SESSION_URL, data=data) as resp:
                rs = await resp.json()
        return rs

    async def sessions_attr_info(self, uid,
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

        async with aiohttp.ClientSession(cookies=self._session.cookies) \
                as session:
            async with session.post(url=SESSION_ATTR_INFO_URL, data=data) as resp:
                rs = await resp.json()
        return rs

    async def find_base(self, page):

        data = {
                "appId": self.app_id,
                "platform": self.platform,
                "json": "[]",
                "page": page,
                "rows": 20,
                "total": 0,
                "order_by": "last_visit_time"
                }
        async with aiohttp.ClientSession(cookies=self._session.cookies) as session:
            async with session.post(url=FIND_URL, data=data) as resp:
                rs = await resp.json()
        # print (result.text)
        return rs

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
                yest_session_path = YEST_SESSION_PATH.\
                    format(platform=self.platform_content,
                           begin_day_id=begin_day_id)
                self.save_file(yest_session_path, datas)
        elif data_type == "Infos":
            info_path = INFO_PATH.format(self.platform_content)
            self.save_file(info_path, datas)

        elif data_type == "Base":
            base_path = BASE_PATH.format(self.platform_content)
            self.save_file(base_path, datas)

    async def get_user_infos_data(self, user_id):
        # deal data by UserInfo mode.

        app_user = {}
        result_js = await self.query_user_info(user_id)

        for name, value in self.build_user_info_data(result_js):
            app_user[name] = value

        return result_js, app_user, result_js["app_data"]["user"]["sessionDays"]

    async def write_user_infos_data(self):
        # deal data by UserInfos mode.

        async for search_user_id in self.get_user_id():
            result_js, app_user, _ = await \
                self.get_user_infos_data(search_user_id)

            result_js["app_data"]["user"]["app_user"] = app_user

            self.write_user_data2file(result_js, data_type="Infos")

    async def get_user_id(self):
        pages = await self.get_page()
        for page in range(1, pages):
            rs = await self.find_base(page)

            for user_data in self.get_user_data(rs):
                yield user_data["zg_id"]

    async def write_base_data(self):
        build_data = {}
        pages = await self.get_page()
        for page in range(1, pages):
            rs = await self.find_base(page)

            for user_data in self.get_user_data(rs):
                build_data["zg_id"] = user_data["zg_id"]
                for k, v in self.build_base_data(user_data):
                    build_data[k] = v
                self.write_user_data2file(build_data, data_type="Base")

    async def get_session_info(self, user_id, session_info):
        if len(session_info["events"]) == 0:
            return
        ip = ""
        column_code = ""
        for index, event in enumerate(session_info["events"]):

            result_json = await self.sessions_attr_info(user_id,
                                                        event["eventId"],
                                                        session_info["sessionId"],
                                                        event["uuid"],
                                                        event["beginDate"])

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

    async def write_sessions_yest_data(self, begin_day_id=None):
        # deal data by sessions mode.

        async for user_id in self.get_user_id():
            result_js = await self.sessions(user_id, begin_day_id)

            for sessionInfo in self.build_sessions_data(result_js):
                sessionInfo["zg_id"] = user_id
                sessionInfo["beginDayId"] = begin_day_id

                async for index, event in self.get_session_info(user_id,
                                                                sessionInfo):
                    sessionInfo["events"][index] = event

                self.write_user_data2file(
                                     sessionInfo,
                                     data_type="Session",
                                     begin_day_id=begin_day_id)

    async def write_sessions_all_data(self):
        # deal data by sessions mode.

        async for user_id in self.get_user_id():

            # get this user dayId
            for begin_day_id in self.get_day_id(user_id):
                # get session data by user_id and beginDayId.
                result_js = await self.sessions(user_id, begin_day_id)

                for sessionInfo in self.build_sessions_data(result_js):
                    sessionInfo["zg_id"] = user_id
                    sessionInfo["beginDayId"] = begin_day_id
                    sessionInfo["events"] = []

                    async for event in self.get_session_info(user_id, sessionInfo):
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

    async def deal_data(self):
        if self.exe_mode[-1] is "1":
            await self.write_base_data()

        if self.exe_mode[-2] is "1":
            await self.write_user_infos_data()

        if self.exe_mode[-3] is "1":
            yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

            begin_day_id = int(yesterday.strftime("%Y%m%d"))
            await self.write_sessions_yest_data(begin_day_id)

        if self.exe_mode[-4] is "1":

            self.write_sessions_all_data()

    async def get_page(self):
        num_dict = await self.find_base(1)
        user_num = num_dict['values']['count']
        page = math.ceil(user_num/20)
        return page + 1

if __name__ == "__main__":

    user_info = UserInfo()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(user_info.deal_data())
    loop.close()
