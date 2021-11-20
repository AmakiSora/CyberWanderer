"""
    下载用户推文图片
"""
import threading
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
def auto_get_user_img(**filter_obj):
    urls = get_img_url(**filter_obj)
    code, statusInfo = multithreading_list(urls, download_file_qiniu, ('', 'default-0', True))
    if code == 0:
        return "无图片上传!"
    elif code == 200:
        return '总共' + str(statusInfo.get('count')) + '张图片!' + \
               '已存在' + str(statusInfo.get('exist')) + '张图片!' + \
               '上传失败' + str(statusInfo.get('fail')) + '张图片!'
    #
    # count = len(urls)
    # if count > 500:
    #     threadNum = 30
    # elif count > 100:
    #     threadNum = 10
    # elif count > 5:
    #     threadNum = 3
    # elif count > 0:
    #     threadNum = 1
    # else:
    #     return "无图片需要下载!"
    # threads = []
    # for i in range(threadNum):
    #     threads.append(threading.Thread(target=loopDownload, args=(urls,)))
    # for i in threads:
    #     i.start()
    # for i in threads:
    #     i.join()
    # return "总共" + str(count) + "张图片"

# def loopDownload(urls):
#     try:
#         url = urls.pop()
#         while url is not None:
#             code, _ = download_file_qiniu(url, isProxy=True)
#             url = urls.pop()
#     except:
#         return
