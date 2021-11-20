"""
    下载工具类
"""
import os

import requests

from CyberWanderer import settings


# 下载图片到本地
def download_file_local(url, file_name='', folder_name=''):
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
                    print("下载成功,url:", url)
                    return 200, file_name
                except:
                    print("下载失败,url：", url)
                    return 500, url
        except:
            print("连接失败!url：", url)
            return 404, url
