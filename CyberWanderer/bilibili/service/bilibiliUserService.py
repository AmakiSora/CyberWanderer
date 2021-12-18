"""
    b用户服务
"""

# 自动获取b用户信息(优先搜索uid)
import json

import requests

from bilibili.models import BiliBiliUser


def autoGetUserInfo(uid, to_db):
    info_json = getUserInfo(uid)
    # '自动获取B站用户信息成功!'
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
        print(uid)
        print(user.name)
        print(user.avatar_url)
        print(user.birthday)
        print(user.sign)
        print(user.level)
        print(user.friends_count)
        print(user.followers_count)
    return '获取成功'
