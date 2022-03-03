"""
    七牛云对象存储工具
"""
import os
import qiniu
import requests
from qiniu import BucketManager
from CyberWanderer import settings

# 下载图片到对象存储(七牛云)
from CyberWanderer.utils.threadUtil import multithreading_list
import logging

logger = logging.getLogger(__name__)


def download_file_qiniu(url, file_name='', bucket_name='default-0', isProxy=False):
    if file_name == '':
        file_name = url.split('/')[-1]
    if qiniu_get_info(file_name, bucket_name) is not None:
        logger.info(str('资源已存在' + str(url)))
        return 'exist', None
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
                logger.info(str("上传到云成功,url:" + str(url)))
                return 'success', None
            except:
                logger.warning(str("上传到云失败,url:" + str(url)))
                return 'fail', None
        else:
            logger.warning(str("资源已失效,url:" + str(url)))
            return 'notExist', None
    except:
        logger.error(str("连接失败!url:" + str(url)))
        return 'fail', None


# 七牛去获取文件存入对象存储(不能翻墙)
def download_qiniu_get(url, file_name='', bucket_name='default-0'):
    bucket = BucketManager(settings.QN)
    # 没有命名就取本身名字
    if file_name == '':
        file_name = url.split('/')[-1]
    re, info = bucket.fetch(url, bucket_name, file_name)
    return 200, re['key']


# 本地文件上传到云
def upload_file_qiniu(local_url, file_name='', bucket_name='default-0'):
    if file_name == '':
        file_name = local_url.split('/')[-1]
    if qiniu_get_info(file_name, bucket_name) is not None:
        logger.info(str('资源已存在' + str(local_url)))
        return 'exist', None
    token = settings.QN.upload_token(bucket_name, file_name, 60)
    re, info = qiniu.put_file(token, file_name, local_url)
    logger.info(str(re))
    if re is None:
        logger.info(str('上传失败!url:' + str(local_url)))
        return 'fail', None
    logger.info('上传成功!url:' + local_url)
    return 'success', None


# 本地文件夹上传到云(多线程)
def upload_folder_qiniu(folder_name, bucket_name='default-0'):
    # a代表所在根目录; b代表根目录下所有文件夹(以列表形式存在); c代表根目录下所有文件
    for a, b, c in os.walk(folder_name):
        urls = []
        for file_name in c:
            local_url = a + '/' + file_name
            urls.append(local_url)
        code, statusInfo = multithreading_list(urls, upload_file_qiniu, ('', bucket_name))
        if code == 0:
            return "无文件上传!"
        elif code == 200:
            return '总共' + str(statusInfo.get('count', 0)) + '张图片!' + \
                   '已存在' + str(statusInfo.get('exist', 0)) + '张图片!' + \
                   '上传成功' + str(statusInfo.get('success', 0)) + '张图片!' + \
                   '上传失败' + str(statusInfo.get('fail', 0)) + '张图片!'


# 获取资源信息(没有返回None)
def qiniu_get_info(file_name, bucket_name='default-0'):
    bucket = BucketManager(settings.QN)
    re, info = bucket.stat(bucket_name, file_name)
    return re

# print(upload_folder_qiniu('D:/cosmos/test/sally_amaki'))  # 本地上传文件
