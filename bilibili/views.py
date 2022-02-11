import json

from django.http import HttpResponse
from bilibili.service import bilibiliUserService, bilibiliDynamicService, bilibiliVideoService, \
    bilibiliImgDownloadService
import logging

logger = logging.getLogger(__name__)


# 自动获取用户信息
def autoGetUserInfo(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        uid = body.get('uid')
        if not uid:
            return HttpResponse('请传入uid参数!')
        to_db = body.get('to_db', True)  # 是否入库
        result = bilibiliUserService.autoGetUserInfo(uid, to_db)
        logger.info(result)
        return HttpResponse(result)


# 自动获取用户动态
def autoGetUserDynamic(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        uid = body.get('uid', '')
        name = body.get('name', '')
        frequency = body.get('frequency', 1)
        to_db = body.get('to_db', True)  # 是否入库
        if uid == '':
            uid = bilibiliUserService.getUidByName(name)
            if uid is None:
                return HttpResponse('请输入name或uid')
        result = bilibiliDynamicService.autoGetUserDynamic(uid, to_db, frequency)
        logger.info(result)
        return HttpResponse(result)


# 自动获取用户所有视频信息
def autoGetUserVideo(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        uid = body.get('uid', '')
        name = body.get('name', '')
        to_db = body.get('to_db', True)  # 是否入库
        if uid == '':
            uid = bilibiliUserService.getUidByName(name)
            if uid is None:
                return HttpResponse('请输入name或uid')
        result = bilibiliVideoService.autoGetUserVideo(uid, to_db)
        logger.info(result)
        return HttpResponse(result)


# 自动获取图片
def autoGetImg(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        filter_obj = body.get('dynamic_param', None)
        if filter_obj is None:
            return HttpResponse("filter_obj不能为空！")
        result = bilibiliImgDownloadService.auto_get_img(**filter_obj)
        logger.info(result)
        return HttpResponse(result)


# 更新多用户动态
def batchUpdateDynamic(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        usernameList = body.get('usernameList', None)
        to_db = body.get('to_db', True)  # 是否入库
        frequency = body.get('frequency', 20)  # 循环次数
        threads = body.get('threads', False)  # 多线程
        if usernameList is None:
            return HttpResponse("名单列表不能为空！")
        elif type(usernameList) is not list:
            return HttpResponse("参数需要为列表！")
        logger.info(usernameList)
        if threads:
            result = bilibiliDynamicService.batchUpdateDynamicThreads(usernameList, to_db, frequency)
            logger.info(result)
            return HttpResponse(result)
        else:
            return HttpResponse('现在只有多线程处理方式！')


# 批量更新用户信息
def batchUpdateBiliBiliUserInfo(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        filter_obj = body.get('bilibili_user_param', None)
        if filter_obj is None:
            return HttpResponse("bilibili_user_param不能为空！")
        result = bilibiliUserService.updateBiliBiliUserInfo(**filter_obj)
        logger.info(result)
        return HttpResponse(result)


# 下载b站视频
def downloadVideo(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        bv = body.get('bv', None)
        if bv is None:
            return HttpResponse("bv不能为空！")
        file_name = body.get('file_name', None)
        folder_name = body.get('folder_name', None)
        proxy = body.get('proxy', False)
        result = bilibiliVideoService.downloadVideo(bv, file_name, folder_name, proxy)
        logger.info(result)
        return HttpResponse(result)
