"""
    b图片下载服务(暂时不用,也没测试过)
"""
from bilibili.models import BiliBiliDynamic


# 取出用户图片链接
def get_img_url(**filter_obj):
    Dynamics = BiliBiliDynamic.objects.filter(**filter_obj)
    all_url_list = []
    for i in Dynamics:
        if i.dynamic_media_urls != '':
            l = i.dynamic_media_urls.split('|')
            l.remove('')
            all_url_list = all_url_list + l
    return all_url_list

