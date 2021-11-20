"""
    七牛云对象存储工具
"""

# 下载图片到对象存储(七牛云)
import qiniu
import requests
from qiniu import BucketManager

from CyberWanderer import settings


def download_file_qiniu(url, file_name='', bucket_name='default-0', isProxy=False):
    if file_name == '':
        file_name = url.split('/')[-1]
    if qiniu_get_info(file_name, bucket_name) is not None:
        print('资源已存在', url)
        return 202, '资源已存在'
    token = settings.QN.upload_token(bucket_name, file_name, 60)
    try:
        if isProxy:
            proxies = settings.PROXIES
        else:
            proxies = None
        r = requests.get(url, proxies=proxies)
        if r.status_code == 200:
            try:
                re, info = qiniu.put_data(token, file_name, data=r.content)
                print("上传到云成功,url:", url)
                return 200, re['key']
            except:
                print("上传到云失败,url:", url)
                return 500, url
    except:
        print("连接失败!url:", url)
        return 404, url


# 七牛去获取文件存入对象存储(不能翻墙)
def download_qiniu_get(url, file_name='', bucket_name='default-0'):
    bucket = BucketManager(settings.QN)
    # 没有命名就取本身名字
    if file_name == '':
        file_name = url.split('/')[-1]
    re, info = bucket.fetch(url, bucket_name, file_name)
    return 200, re['key']


# 获取资源信息
def qiniu_get_info(file_name, bucket_name='default-0'):
    bucket = BucketManager(settings.QN)
    re, info = bucket.stat(bucket_name, file_name)
    return re
