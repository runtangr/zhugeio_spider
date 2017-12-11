# coding: utf-8
from ftplib import FTP
import time
import tarfile
import os
import datetime
from config import PLATFORM

from ftplib import FTP


def ftp_connect(host, username, password):
    ftp = FTP()
    # ftp.set_debuglevel(2)
    ftp.connect(host, 21)
    ftp.login(username, password)
    return ftp


# 从本地上传文件到ftp
def uploadfile(ftp_fd, remotepath, localpath):
    buf_size = 1024
    fp = open(localpath, 'rb')
    ftp.storbinary('STOR ' + remotepath, fp, buf_size)
    ftp_fd.set_debuglevel(0)
    fp.close()

if __name__ == "__main__":
    ftp = ftp_connect("10.3.131.138", "zhugeio", "123456")

    base_dir = os.path.dirname(__file__)
    begin_day_id = (datetime.datetime.now()
                    - datetime.timedelta(days=1)).strftime("%Y%m%d")
    platform = int(os.getenv("PLATFORM"))


    uploadfile(ftp, "/app/ftp/zhugeio/UserSession{0}_{1}.csv"
               .format(PLATFORM[platform], begin_day_id),
               "{0}/filter_info/UserSession{1}_{2}.csv"
               .format(base_dir, PLATFORM[platform], begin_day_id))

    ftp.quit()
