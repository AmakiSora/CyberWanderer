import json

from django.http import HttpResponse
from bilibili.service import bilibiliUserService


# 自动获取用户信息
def autoGetUserInfo(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        uid = body.get('uid')
        if not uid:
            return HttpResponse('请传入uid参数!')
        to_db = body.get('to_db', True)  # 是否入库
        return HttpResponse(bilibiliUserService.autoGetUserInfo(uid, to_db))

