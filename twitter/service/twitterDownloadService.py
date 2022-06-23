"""
    用户推文图片下载服务
"""

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


# 下载推文视频
def downloadVideo(id, file_name, folder_name, proxy):
    url = 'https://twitter.com/i/status/' + id
    return downloadUtils.download_file_local(url, file_name, folder_name, proxy)
