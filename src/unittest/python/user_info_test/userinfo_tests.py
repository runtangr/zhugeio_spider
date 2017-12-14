
#encoding=utf-8
#!/usr/bin/env python3
__author__ = 'tangr'

import unittest
import copy
class userInfo(unittest.TestCase):

    def test_many_execMode(self):
        pass
        # platform = 1
        # # page = 2
        #
        # currentUser()
        #
        # # test find.jsp.
        # # find(page,platform)
        #
        # # test find userid.
        # # for userid in getUserid(platform):
        # #     print(userid)
        #
        # # test write base data.
        # # writeBase(platform)
        #
        # exec_mode = "000100"
        # dealData(platform, exec_mode)
    def test_userbase(self):
        pass

    def test_userid(self):
        pass

    def test_write_base_data(self):
        pass

    def test_deep_copy(self):
        value = {'sessionId': '1513034189667',
                 'beginDate': 1513034189000,
                 'events': [{'eventId': 24060186, 'eventName': '首页-底部功能栏',
                             'beginDate': 1513034191000, 'uuid': '7a68a1b897844aaa975fa8bd9aa0c9f5'},
                            {'eventId': 24060125, 'eventName': '进入首页', 'beginDate': 1513034194000,
                             'uuid': 'e4005fd2d3ca469fa3a1780e4836a424'}]
                 }
        write_value = copy.deepcopy(value)
        write_value['events'] = []
        print(value)
        print(write_value)