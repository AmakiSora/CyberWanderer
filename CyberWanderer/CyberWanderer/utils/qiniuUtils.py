"""
    七牛云对象存储工具
"""
import os
import threading

import qiniu
import requests
from qiniu import BucketManager
from CyberWanderer import settings

# 下载图片到对象存储(七牛云)
from CyberWanderer.utils.threadUtil import multithreading_list


def download_file_qiniu(url, file_name='', bucket_name='default-0', isProxy=False):
    if file_name == '':
        file_name = url.split('/')[-1]
    if qiniu_get_info(file_name, bucket_name) is not None:
        print('资源已存在', url)
        return 'exist'
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
                return '1'
            except:
                print("上传到云失败,url:", url)
                return 'fail'
    except:
        print("连接失败!url:", url)
        return 'fail'


# 七牛去获取文件存入对象存储(不能翻墙)
def download_qiniu_get(url, file_name='', bucket_name='default-0'):
    bucket = BucketManager(settings.QN)
    # 没有命名就取本身名字
    if file_name == '':
        file_name = url.split('/')[-1]
    re, info = bucket.fetch(url, bucket_name, file_name)
    return 200, re['key']


# # 本地文件上传到云
# def upload_file_qiniu(local_url, statusInfo, file_name='', bucket_name='default-0'):
#     if file_name == '':
#         file_name = local_url.split('/')[-1]
#     if qiniu_get_info(file_name, bucket_name) is not None:
#         print('资源已存在', local_url)
#         statusInfo['exist'] = statusInfo['exist'] + 1
#         return '资源已存在' + local_url
#     token = settings.QN.upload_token(bucket_name, file_name, 60)
#     re, info = qiniu.put_file(token, file_name, local_url)
#     print(re)
#     if re is None:
#         statusInfo['fail'] = statusInfo['fail'] + 1
#         print('上传失败!url:' + local_url)
#         return '上传失败!url:' + local_url
#     return '上传成功!url:' + local_url

# 本地文件上传到云
def upload_file_qiniu(local_url, file_name='', bucket_name='default-0'):
    if file_name == '':
        file_name = local_url.split('/')[-1]
    if qiniu_get_info(file_name, bucket_name) is not None:
        print('资源已存在', local_url)
        return 'exist'
    token = settings.QN.upload_token(bucket_name, file_name, 60)
    re, info = qiniu.put_file(token, file_name, local_url)
    print(re)
    if re is None:
        print('上传失败!url:' + local_url)
        return 'fail'
    return '上传成功!url:' + local_url


# 本地文件夹上传到云(多线程)
def upload_folder_qiniu(folder_name, bucket_name='default-0'):
    # a代表所在根目录; b代表根目录下所有文件夹(以列表形式存在); c代表根目录下所有文件
    for a, b, c in os.walk(folder_name):
        urls = []
        for file_name in c:
            local_url = a + '/' + file_name
            urls.append(local_url)
        code, statusInfo = multithreading_list(urls, upload_file_qiniu)
        if code == 0:
            return "无文件上传!"
        elif code == 200:
            return '总共' + str(statusInfo.get('count')) + '张图片!' + \
                   '已存在' + str(statusInfo.get('exist')) + '张图片!' + \
                   '上传失败' + str(statusInfo.get('fail')) + '张图片!'
        # count = len(urls)
        # print(count)
        # if count > 500:
        #     threadNum = 20
        # elif count > 100:
        #     threadNum = 10
        # elif count > 5:
        #     threadNum = 3
        # elif count > 0:
        #     threadNum = 1
        # else:
        #     return "无文件上传!"
        # threads = []
        # statusInfo = {'exist': 0, 'fail': 0}
        # for i in range(threadNum):
        #     threads.append(threading.Thread(target=loopUpload, args=(urls, statusInfo, bucket_name)))
        # for i in threads:
        #     i.start()
        # for i in threads:
        #     i.join()
        # return '总共' + str(count) + '张图片!' + \
        #        '已存在' + str(statusInfo.get('exist')) + '张图片!' + \
        #        '上传失败' + str(statusInfo.get('fail')) + '张图片!'


# def loopUpload(urls, statusInfo, bucket_name):
#     try:
#         url = urls.pop()
#         while url is not None:
#             upload_file_qiniu(url, statusInfo, bucket_name=bucket_name)
#             url = urls.pop()
#     except:
#         return


# 获取资源信息(没有返回None)
def qiniu_get_info(file_name, bucket_name='default-0'):
    bucket = BucketManager(settings.QN)
    re, info = bucket.stat(bucket_name, file_name)
    return re

# print(upload_folder_qiniu('D:/cosmos/test/sally_amaki'))  # 本地上传文件
