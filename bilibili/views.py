import json

from django.http import HttpResponse
from bilibili.service import bilibiliUserService, bilibiliDynamicService, bilibiliVideoService, \
    bilibiliImgDownloadService


# 自动获取用户信息
def autoGetUserInfo(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        uid = body.get('uid')
        if not uid:
            return HttpResponse('请传入uid参数!')
        to_db = body.get('to_db', True)  # 是否入库
        return HttpResponse(bilibiliUserService.autoGetUserInfo(uid, to_db))


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
        return HttpResponse(bilibiliDynamicService.autoGetUserDynamic(uid, to_db, frequency))


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
        return HttpResponse(bilibiliVideoService.autoGetUserVideo(uid, to_db))


# 自动获取图片
def autoGetImg(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        filter_obj = body.get('dynamic_param', None)
        if filter_obj is None:
            return HttpResponse("filter_obj不能为空！")
        return HttpResponse(bilibiliImgDownloadService.auto_get_img(**filter_obj))
