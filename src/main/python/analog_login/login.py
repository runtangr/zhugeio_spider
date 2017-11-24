#encoding=utf-8
#!/usr/bin/env python3
'''
auther: tangr
'''

import requests
import json
import time
import os

def login():

	url = "https://zhugeio.com/index/loginActionJsonp.jsp?jsonpcallback=jQuery21406835245867372233_{0}".format(int(time.time()*1000))

	header = {
			"Accept":"text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",

			"Host":"zhugeio.com",

			"Origin":"https://zhugeio.com", 

			"Referer":"https://zhugeio.com/index/login.jsp",

			"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36X-Requested-With:XMLHttpRequest"
			}

	jsondata = {"username":os.environ.get("username"),"password":os.environ.get("password"),"type":0,"location":""}
	send_data = {"data": json.dumps(jsondata)}

	result = requests.get("https://zhugeio.com/index/login.jsp")
	cookies = dict(JSESSIONID=result.cookies["JSESSIONID"])

	results = requests.post(url, headers=header,data=send_data, cookies=cookies)

	return result.cookies


if __name__ == '__main__':
	login()