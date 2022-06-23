"""
    下载工具类
"""
import os
import sys

import requests
import you_get

from CyberWanderer import settings
import logging

from CyberWanderer.utils.qiniuUtils import download_file_qiniu
from CyberWanderer.utils.threadUtil import multithreading_list

logger = logging.getLogger(__name__)


# 下载图片到本地
def download_img_local(url, file_name='', folder_name='', useProxy=False):
    if folder_name == '':
        folder_name = '/static/img'
    if file_name == '':
        file_name = url.split('/')[-1]
    # 校验文件是否已存在
    if os.path.isfile(folder_name + file_name):
        logger.info(str('资源已存在' + str(url)))
        return 'exist', None
    try:
        if useProxy:
            proxies = settings.PROXIES
        else:
            proxies = None
        r = requests.get(url, proxies=proxies)
        if r.status_code == 200:
            try:
                open(folder_name + file_name, 'wb').write(r.content)
                logger.info(str("下载成功,url:" + str(url)))
                return 'success', None
            except:
                logger.warning(str("下载失败,url：" + str(url)))
                return 'fail', None
        else:
            logger.warning(str("资源已失效,url:" + str(url)))
            return 'notExist', None
    except:
        logger.error(str("连接失败!url：" + str(url)))
        return 'fail', None


# 下载资源到本地(you-get)
def download_file_local(url, file_name='', folder_name='', proxy=False):
    order = ['you-get']
    # 本地路径
    if folder_name:
        order.append('-o')
        order.append(folder_name)
    else:
        # 默认文件夹
        order.append('-o')
        order.append(str(settings.DOWNLOAD_PATH))
    # 文件名(需自带后缀)
    if file_name:
        order.append('-O')
        order.append(file_name)
    # 代理设置
    if proxy:
        order.append('-x')
        order.append('127.0.0.1:7890')
    order.append(url)
    logger.info('youGet执行命令->' + ' '.join(order))
    sys.argv = order
    you_get.main()
    return 'OK'


# 自动获取图片
def auto_get_img(urls, download_method):
    if download_method.get('method', 'qiniu') == 'qiniu':
        code, statusInfo = multithreading_list(urls,
                                               download_file_qiniu,
                                               ('', download_method.get('bucket_name', 'default-0'),
                                                download_method.get('useProxy', False)))
        if code == 0:
            return "无图片上传!"
        elif code == 200:
            return '总共' + str(statusInfo.get('count', 0)) + '张图片!' + \
                   '已存在' + str(statusInfo.get('exist', 0)) + '张图片!' + \
                   '已失效' + str(statusInfo.get('notExist', 0)) + '张图片!' + \
                   '上传成功' + str(statusInfo.get('success', 0)) + '张图片!' + \
                   '上传失败' + str(statusInfo.get('fail', 0)) + '张图片!'
    elif download_method.get('method') == 'local':
        code, statusInfo = multithreading_list(urls, download_img_local,
                                               ('', download_method.get('local_url', ''),
                                                download_method.get('useProxy', False)))
        if code == 0:
            return "无图片上传!"
        elif code == 200:
            return '总共' + str(statusInfo.get('count', 0)) + '张图片!' + \
                   '已存在' + str(statusInfo.get('exist', 0)) + '张图片!' + \
                   '已失效' + str(statusInfo.get('notExist', 0)) + '张图片!' + \
                   '下载成功' + str(statusInfo.get('success', 0)) + '张图片!' + \
                   '下载失败' + str(statusInfo.get('fail', 0)) + '张图片!'
