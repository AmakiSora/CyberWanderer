"""
    用户推文图片下载服务
"""
import json

from CyberWanderer.utils import downloadUtils
from CyberWanderer.utils.qiniuUtils import download_file_qiniu
from CyberWanderer.utils.threadUtil import multithreading_list
from twitter.models import Tweet


# 取出用户图片链接
def get_img_url(**filter_obj):
    tweets = Tweet.objects.filter(**filter_obj)
    all_url_list = []
    for i in tweets:
        if i.tweet_media_urls != '':
            l = i.tweet_media_urls.split('|')
            l.remove('')
            all_url_list = all_url_list + l
    return all_url_list


# 自动获取用户图片
def auto_get_img(**filter_obj):
    urls = get_img_url(**filter_obj)
    code, statusInfo = multithreading_list(urls, download_file_qiniu, ('', 'default-0', True))
    if code == 0:
        return "无图片上传!"
    elif code == 200:
        return '总共' + str(statusInfo.get('count')) + '张图片!' + \
               '已存在' + str(statusInfo.get('exist')) + '张图片!' + \
               '上传成功' + str(statusInfo.get('success')) + '张图片!' + \
               '上传失败' + str(statusInfo.get('fail')) + '张图片!'


# 下载推文视频
def downloadVideo(id, file_name, folder_name, proxy):
    url = 'https://twitter.com/i/status/' + id
    return downloadUtils.download_file_local(url, file_name, folder_name, proxy)
