
ZHUGEIO_URL = 'https://zhugeio.com'
LOGIN_URL = 'https://zhugeio.com/index/loginActionJsonp.jsp?jsonpcallback'
CURRENT_USER = 'https://zhugeio.com/company/currentUser.jsp'
FIND_URL = 'https://zhugeio.com/appuser/find.jsp'
USER_INFO_URL = 'https://zhugeio.com/appuser/queryUserInfos.jsp'
SESSION_URL = 'https://zhugeio.com/appuser/sessions.jsp'
SESSION_ATTR_INFO_URL = 'https://zhugeio.com/appuser/querySessionAttrInfos.jsp'
APP_INFO = 'https://zhugeio.com/data/v2ajaxGetDataByApp.jsp'

TOKEN_FILE = 'token.json'

CLIENT_ID = '8d5227e0aaaa4797a763ac64e0c3b8'

FIELD_NAMES = ['Userid', 'fwDatetime',
               'qxmc', 'fwIP',
               'fwSource', 'fwCode']

INFO_DIR = './info/'
FILTER_INFO_DIR = './filter_info/'

FILTER_PATH = './filter_info/UserSession{platform}_{begin_day_id}.csv'
INFO_PATH = './info/Infos{}.json'
BASE_PATH = './info/Base{}.json'
ALL_SESSION_PATH = './info/Session{}_all.json'
YEST_SESSION_PATH = './info/Session{platform}_{begin_day_id}.json'

INFO_TYPE = ['Base', 'Infos', 'Session']

PLATFORM = {
            1: "Android",
            2: "Ios",
            3: "PC"
        }
