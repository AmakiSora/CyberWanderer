'''
    下载用户推文图片
'''
import requests

from twitter.models import TwitterUser, Tweet


# 取出用户图片链接
def get_img_url(**filter_obj):
    tweets = Tweet.objects.filter(**filter_obj)
    all_url_list = []
    for i in tweets:
        if (i.tweet_media_urls != ''):
            list = i.tweet_media_urls.split('|')
            list.remove('')
            all_url_list = all_url_list + list
    return all_url_list


# 下载图片
def download_img(url, folder_name=''):
    if folder_name == '':
        folder_name = 'C:/download/TwitterImg/all/'
    file_name = url.split('/')[-1]
    try:
        r = requests.get(url)
        if r.status_code == 200:
            try:
                open(folder_name + file_name, 'wb').write(r.content)
                print("下载成功,url:", url)
            except:
                print("下载失败,url：", url)

    except:
        print("下载失败!")


# 自动获取用户图片
def auto_get_user_img(folder_name='', **filter_obj):
    for i in get_img_url(**filter_obj):
        download_img(i, folder_name)
