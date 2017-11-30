# -*- coding:utf-8 -*-

import datetime
import csv
import json
import time

'''
    function: filter user data and save to csv.
'''


class FilterInfo(object):
    def __init__(self):
        day_id = (datetime.datetime.now()
                  ).strftime("%Y%m%d")
        self.data_type = "Session"
        self.plat = {
            1: "Android",
            2: "Ios",
            3: "PC"
        }
        self.plat_form = 3

        self.beginDayId = day_id

    def read_session(self, zg_id):
        with open('./user_file/{data_type}{platform}_{beginDayId}.json'.format(
                data_type=self.data_type,
                platform=self.plat[self.plat_form],
                beginDayId=self.beginDayId),
                  'r') as f:
            for read_line in f:
                line_dic = json.loads(read_line)
                if line_dic["zg_id"] == zg_id:
                    yield line_dic

    def read_user_info(self):
        with open('./user_file/UserInfos{platform}.json'.format(
                platform=self.plat[self.plat_form]),
                  'r') as f:

            for read_line in f:
                line_dic = json.loads(read_line)

                yield (line_dic["app_data"]["user"]["app_user"]["zg_id"],
                       line_dic["app_data"]["user"]["app_user"]["app_user_id"])

    def init_write_csv(self):
        with open('./user_filter/UserSession{platform}.csv'.format(
                platform=self.plat[self.plat_form]),
                'a') as csv_file:
            fieldnames = ["user_id", "event_time",
                          "event_content", "ip",
                          "platform", "encode"]

            writer = csv.DictWriter(csv_file, fieldnames)
            writer.writerow({"user_id": "user_id",
                             "event_time": "event_time",
                             "event_content": "event_content",
                             "ip": "ip",
                             "platform": "platform",
                             "encode": "encode"})

    def write_csv(self, user_id, events):
        with open('./user_filter/UserSession{platform}.csv'.format(
                platform=self.plat[self.plat_form]),
                'a') as csv_file:
            fieldnames = ["user_id", "event_time",
                          "event_content", "ip",
                          "platform", "encode"]
            writer = csv.DictWriter(csv_file, fieldnames)
            for event in events:
                time_array = time.localtime(event["beginDate"]/1000)
                str_style_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)

                writer.writerow({"user_id": user_id,
                                 "event_time": str_style_time,
                                 "event_content": event["eventName"],
                                 "ip": event["ip"],
                                 "platform": (5 if self.plat_form == 3
                                              else self.plat_form),
                                 "encode": str(event["column_code"])})

    def write_filter_info(self):
        for search_zg_id, search_user_id in self.read_user_info():
            # filter user.
            if search_user_id is not None:
                for line in self.read_session(search_zg_id):
                    # filter events.
                    if len(line["events"]) is 0:
                        continue
                    # write user events data.
                    self.write_csv(user_id=search_user_id,
                                   events=line["events"])

if __name__ == "__main__":

    filter_info = FilterInfo()
    filter_info.init_write_csv()
    filter_info.write_filter_info()
