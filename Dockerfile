FROM python:3.6.3

ADD ./src /app/src
ADD requirements.txt /app/requirements.txt

workdir /app/
RUN pip install -r requirements.txt

workdir /app/src/main/python/user_info

