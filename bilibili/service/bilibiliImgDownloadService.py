"""
    b图片下载服务(暂时不用,也没测试过)
"""
from CyberWanderer.utils.qiniuUtils import download_file_qiniu
from CyberWanderer.utils.threadUtil import multithreading_list
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


# 自动获取图片
def auto_get_img(**filter_obj):
    urls = get_img_url(**filter_obj)
    code, statusInfo = multithreading_list(urls, download_file_qiniu, ('', 'default-0', True))
    if code == 0:
        return "无图片上传!"
    elif code == 200:
        return '总共' + str(statusInfo.get('count', 0)) + '张图片!' + \
               '已存在' + str(statusInfo.get('exist', 0)) + '张图片!' + \
               '上传成功' + str(statusInfo.get('success', 0)) + '张图片!' + \
               '上传失败' + str(statusInfo.get('fail', 0)) + '张图片!'
