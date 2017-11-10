#encoding=utf-8
'''
auther: tangr
'''

import requests
import json

def login():


	url = "https://zhugeio.com/index/loginActionJsonp.jsp?jsonpcallback=jQuery21406835245867372233_1510219976704"

	header = {
			"Accept":"text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",

			"Host":"zhugeio.com",

			"Origin":"https://zhugeio.com", 

			"Referer":"https://zhugeio.com/index/login.jsp",

			"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36X-Requested-With:XMLHttpRequest"}

	send_data = {"username":"17708192660","password":"wrfDoMOTwrU8w63DpQ3CqWlfTg==","type":0,"location":""}

	results = requests.post(url, headers=header,data=send_data)
	print(results.text)


	# url = 'https://api.github.com/some/endpoint'
	# payload = {'some': 'data'}
	# headers = {'content-type': 'application/json'}

	# r = requests.post(url, data=json.dumps(payload), headers=headers)
	# print r.text

	def login_page():

		url = "https://zhugeio.com/index/login.jsp"

		session_requests = requests.session()


		send_data = {"username":"17708192660","password":"wrfDoMOTwrU8w63DpQ3CqWlfTg==","type":0,"location":""}

		results = requests.post(url, headers=header,data=send_data)
		print(results.text)

if __name__ == '__main__':
	login()