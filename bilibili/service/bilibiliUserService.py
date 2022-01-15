"""
    b用户服务
"""

import json

import requests

from bilibili.models import BiliBiliUser
import logging

from bilibili.service import bilibiliDynamicService, bilibiliVideoService

logger = logging.getLogger(__name__)


# 自动获取b用户信息(优先搜索uid)
def autoGetUserInfo(uid, to_db):
    info_json = getUserInfo(uid)
    return analyzeUserInfo(info_json, to_db)


# 获取用户信息json
def getUserInfo(uid):
    u = 'https://api.bilibili.com/x/space/acc/info'
    params = {
        'mid': uid
    }
    info_json = requests.get(u, params)
    if info_json.status_code == 200:
        return json.loads(info_json.text)
    return None


# 获取用户粉丝与关注
def getUserFollow(uid):
    u = 'https://api.bilibili.com/x/relation/stat'
    params = {
        'vmid': uid
    }
    info_json = requests.get(u, params)
    if info_json.status_code == 200:
        j = json.loads(info_json.text)
        if j.get('code') != 0:
            return 0, 0
        data = j.get('data')
        return data.get('following', 0), data.get('follower', 0)
    return None


# 解析用户信息json
def analyzeUserInfo(info_json, to_db):
    if info_json.get('code') != 0:
        return '用户不存在'
    user = BiliBiliUser()
    data = info_json.get('data')
    uid = data.get('mid')
    user.uid = uid
    user.name = data.get('name')
    user.avatar_url = data.get('face')
    user.birthday = data.get('birthday', '')
    user.sign = data.get('sign')
    user.level = data.get('level')
    user.friends_count, user.followers_count = getUserFollow(uid=uid)
    if to_db:
        user.save()
    else:
        logger.info(str(uid))
        logger.info(str(user.name))
        logger.info(str(user.avatar_url))
        logger.info(str(user.birthday))
        logger.info(str(user.sign))
        logger.info(str(user.level))
        logger.info(str(user.friends_count))
        logger.info(str(user.followers_count))
    bilibiliDynamicService.updateDynamicCount(uid)
    bilibiliVideoService.updateVideoCount(uid)
    return 'uid : ' + str(uid) + ', up : ' + user.name


# 根据name从数据库中取出uid
def getUidByName(name):
    try:
        uid = BiliBiliUser.objects.get(name=name).uid
    except:
        return None
    return uid


def updateBiliBiliUserInfo(**filter_obj):
    bilibili_users = BiliBiliUser.objects.filter(**filter_obj)
    if bilibili_users.count() == 0:
        return '未找到筛选的用户!!!'
    msg = '共更新了 ' + str(bilibili_users.count()) + ' 个用户信息\n'
    for info in bilibili_users:
        re = autoGetUserInfo(info.uid, True)
        msg += re + '\n'
        logger.info(re)
    return msg
