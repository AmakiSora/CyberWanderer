"""
    下载工具类
"""
import os
import sys

import requests
import you_get

from CyberWanderer import settings
import logging

logger = logging.getLogger(__name__)


# 下载图片到本地
def download_img_local(url, file_name='', folder_name=''):
    if folder_name == '':
        folder_name = '/static/img'
    if file_name == '':
        file_name = url.split('/')[-1]
    if not os.path.isfile(folder_name + file_name):
        try:
            r = requests.get(url, proxies=settings.PROXIES)
            if r.status_code == 200:
                try:
                    open(folder_name + file_name, 'wb').write(r.content)
                    logger.info(str("下载成功,url:" + str(url)))
                    return 200, file_name
                except:
                    logger.warning(str("下载失败,url：" + str(url)))
                    return 500, url
        except:
            logger.error(str("连接失败!url：" + str(url)))
            return 404, url


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
