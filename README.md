# 主要运用技术
      session
      requests
      生成器
      token (模块已添加，目前诸葛io响应没有token)
      asyncio
      aiohttp

# 主要需求
      通过ajax 接口获取所有用户id,通过用户id获取用户数据
      用户基础数据,解析存储
      单个用户具体数据,解析存储

# 主要实现目标
      1.模拟登录，保持session
      2.异步协程获取所以用户数据，保存json文件
      3.过滤用户数据保存csv文件

# 代码说明
    src/main/python/user_info
        client.py   模拟用户登录诸葛io
        config.py   配置请求诸葛io的url, 存储csv 格式定义, 存储json定义
        crawl.py    诸葛io 用户数据爬取，解析，存储json
        filterinfo.py   过滤json 数据存储 csv文件
        ftp.py      csv文件上传ftp服务器
        exception.py    自定义异常

# 生产环境使用
    docker-compose up -d

# 遇到问题
      1.返回非json数据  text/html
       策略:
           1.1 请求加头
           1.2 延时，重新请求




