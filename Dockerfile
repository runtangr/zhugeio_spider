FROM python:3.6

ADD ./src /app/src
ADD requirements.txt /app/requirements.txt

workdir /app/
RUN pip install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
RUN pip install aiohttp==2.3.6

workdir /app/src/main/python/user_info

