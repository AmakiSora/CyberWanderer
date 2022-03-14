"""
    b动态服务
"""
import datetime
import json

import requests
import logging

from CyberWanderer.utils.threadUtil import multithreading_list
from bilibili.models import BiliBiliDynamic, BiliBiliUser
from bilibili.service import bilibiliUserService

logger = logging.getLogger(__name__)


# 自动获取b用户动态(优先搜索uid)
def autoGetUserDynamic(uid, to_db=True, frequency=1):
    data_json = getUserDynamic(uid)
    has_more, next_offset = analyzeUserDynamic(data_json, to_db)
    if frequency > 1:
        for i in range(frequency):
            data_json = getUserDynamic(uid, next_offset)
            # 无后续或出错!
            if has_more != 1:
                oldCount, newCount = updateDynamicCount(uid)
                return 'uid: ' + str(uid) + \
                       ' 新增 ' + str(newCount - oldCount) + ' 条动态!' + \
                       ' 总共 ' + str(newCount) + ' 条动态!'
            has_more, next_offset = analyzeUserDynamic(data_json, to_db)
    oldCount, newCount = updateDynamicCount(uid)
    return 'uid: ' + str(uid) + \
           ' 新增 ' + str(newCount - oldCount) + ' 条动态!' + \
           ' 总共 ' + str(newCount) + ' 条动态!'


# 获取动态json
def getUserDynamic(uid, offset_dynamic_id=0):
    u = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history'
    params = {
        'host_uid': uid,
        'need_top': 0,
        'offset_dynamic_id': offset_dynamic_id
    }
    data_json = requests.get(u, params)
    if data_json.status_code == 200:
        logger.info(data_json.text)
        return json.loads(data_json.text)
    return None


# 分析动态json
def analyzeUserDynamic(data_json, to_db):
    if data_json.get('code') != 0:
        return 0, '没有获取到动态!'
    data = data_json.get('data')
    cards = data.get('cards')
    dynamics = []
    dynamicNum = 0  # 记录动态数
    if cards is not None:
        for card in cards:
            d = BiliBiliDynamic()
            d.dynamic_id = card['desc']['dynamic_id']
            d.name = card['desc']['user_profile']['info']['uname']
            d.uid = card['desc']['user_profile']['info']['uid']
            d.created_time = datetime.datetime.fromtimestamp(card['desc']['timestamp'])
            d.dynamic_type = card['desc']['type']
            # 1:动态转发
            if d.dynamic_type == 1:
                c = json.loads(card['card'])
                d.full_text = c['item']['content']
                d.quoted_dynamic_id = c['item']['orig_dy_id']
                # 转发的动态另存
                quoted_dynamic = getQuotedDynamic(card['desc']['origin'], c, c['item']['orig_type'])
                dynamics.append(quoted_dynamic)
            # 2:自己发表的动态
            elif d.dynamic_type == 2:
                c = json.loads(card['card'])
                d.full_text = c['item']['description']
                pictures = c['item'].get('pictures')
                if pictures is not None:
                    for p in pictures:
                        d.dynamic_media_urls = d.dynamic_media_urls + '|' + p.get('img_src')
            # 4:自己发表的无图片动态
            elif d.dynamic_type == 4:
                c = json.loads(card['card'])
                d.full_text = c['item']['content']
            # 8:视频投稿
            elif d.dynamic_type == 8:
                c = json.loads(card['card'])
                d.full_text = c['dynamic']
                d.bvid = card['desc']['bvid']
            # 64:专栏
            elif d.dynamic_type == 64:
                d.full_text = card
            # 256:音乐
            elif d.dynamic_type == 256:
                d.full_text = card
            # 512:动漫影剧
            elif d.dynamic_type == 512:
                d.full_text = card
            # 1024:源动态已被作者删除
            elif d.dynamic_type == 1024:
                d.full_text = card
            # 2048:演唱会
            elif d.dynamic_type == 2048:
                d.full_text = card
            # 4099:综艺,例:589592498855379800
            elif d.dynamic_type == 4099:
                d.full_text = card
            # 4200:结束了的直播,例:414318706021128124
            elif d.dynamic_type == 4200:
                d.full_text = card
            # 4300:合集,例:353559964051664217
            elif d.dynamic_type == 4300:
                d.full_text = card
            # 4308:直播
            elif d.dynamic_type == 4308:
                d.full_text = card
            else:
                logger.warning('有其他类型,解决一下!' + d.dynamic_type)
                logger.warning(card)
                d.full_text = card
            dynamics.append(d)
            dynamicNum += 1
        if to_db:
            BiliBiliDynamic.objects.bulk_create(dynamics, ignore_conflicts=True)  # 批量存入数据库(忽略重复id,即不会更新数据)
        else:
            for i in dynamics:
                logger.info(i.dynamic_id)
                logger.info(i.dynamic_type)
                logger.info(i.name)
                logger.info(i.uid)
                logger.info(i.full_text)
                logger.info(i.created_time)
                logger.info('-------------------------------------------------------')
    logger.info('本次共获取 ' + str(dynamicNum) + '条动态')
    has_more = data.get('has_more', 0)
    next_offset = data.get('next_offset', None)
    return has_more, next_offset


# 处理被转发的动态信息
def getQuotedDynamic(origin, card, dynamic_type):
    qd = BiliBiliDynamic()
    qd.dynamic_id = origin['dynamic_id_str']
    qd.dynamic_type = dynamic_type
    qd.created_time = datetime.datetime.fromtimestamp(origin['timestamp'])
    # 2:自己发表的动态
    if dynamic_type == 2:
        co = json.loads(card['origin'])
        qd.full_text = co['item']['description']
        qd.uid = co['user']['uid']
        qd.name = co['user']['name']
        pictures = co['item'].get('pictures')
        if pictures is not None:
            for p in pictures:
                qd.dynamic_media_urls = qd.dynamic_media_urls + '|' + p.get('img_src')
    # 4:自己发表的无图片动态
    elif dynamic_type == 4:
        co = json.loads(card['origin'])
        qd.full_text = co['item']['content']
        qd.uid = co['user']['uid']
        qd.name = co['user']['uname']
    # 8:视频投稿
    elif dynamic_type == 8:
        qd.bvid = origin['bvid']
        co = json.loads(card['origin'])
        qd.full_text = co['dynamic']
        qd.uid = co['owner']['mid']
        qd.name = co['owner']['name']
    else:
        logger.warning('有新被转发动态类型,请处理!!!' + str(dynamic_type))
        logger.warning(card)
        qd.full_text = card
    return qd


# 批量更新用户动态(多线程)
def batchUpdateDynamicThreads(usernameList, to_db, frequency):
    code, statusInfo = multithreading_list(usernameList, batchUpdateDynamicThreadFunction,
                                           (to_db, frequency))
    if code == 0:
        return "无!"
    elif code == 200:
        re = ['总共' + str(statusInfo.get('count', 0)) + '个用户!']
        for i in statusInfo:
            if i != 'count':
                re.append(statusInfo[i])
        return re


# 多线程处理方法
def batchUpdateDynamicThreadFunction(username, to_db, frequency):
    uid = bilibiliUserService.getUidByName(username)
    if uid is None:
        logger.info(username + '在数据库中不存在!')
        return 'fail', None
    logger.info("更新用户" + username + "的推文")
    re = autoGetUserDynamic(uid, to_db, frequency)
    oldCount, newCount = updateDynamicCount(uid)
    logger.info('用户：' + username + ' 更新了 ' + str(newCount - oldCount) + ' 条动态,现存 ' + str(newCount) + ' 条动态！')
    return username, re


# 更新动态数
def updateDynamicCount(uid):
    t = BiliBiliUser.objects.get(uid=uid)
    oldCount = t.dynamic_count
    newCount = BiliBiliDynamic.objects.filter(uid=uid).count()
    t.dynamic_count = newCount
    t.save()
    return oldCount, newCount
