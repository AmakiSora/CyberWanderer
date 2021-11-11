'''
    下载用户推文图片
'''
import os
import threading

import requests

from twitter.models import TwitterUser, Tweet


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


# 下载图片
def download_img(url, folder_name=''):
    if folder_name == '':
        folder_name = 'C:/download/TwitterImg/all/'
    file_name = url.split('/')[-1]
    if not os.path.isfile(folder_name + file_name):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                try:
                    open(folder_name + file_name, 'wb').write(r.content)
                    print("下载成功,url:", url)
                except:
                    print("下载失败,url：", url)
        except:
            print("连接失败!url：", url)


# 自动获取用户图片
def auto_get_user_img(folder_name='', **filter_obj):
    urls = get_img_url(**filter_obj)
    count = len(urls)
    if count > 500:
        threadNum = 20
    elif count > 100:
        threadNum = 10
    elif count > 5:
        threadNum = 3
    else:
        return "无图片需要下载!"
    threads = []
    for i in range(threadNum):
        threads.append(threading.Thread(target=loopDownload, args=(urls, folder_name)))
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    return "总共" + str(count) + "张图片"


def loopDownload(urls, folder_name):
    try:
        url = urls.pop()
        while url is not None:
            download_img(url, folder_name)
            url = urls.pop()
    except:
        return
