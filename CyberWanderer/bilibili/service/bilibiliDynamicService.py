"""
    b动态服务
"""
import datetime
import json
import time

import requests
import logging

from bilibili.models import BiliBiliDynamic

logger = logging.getLogger(__name__)


# 自动获取b用户信息(优先搜索uid)
def autoGetUserDynamic(uid, to_db):
    data_json = getUserDynamic(uid)
    return analyzeUserDynamic(data_json, to_db)


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


def analyzeUserDynamic(data_json, to_db):
    if data_json.get('code') != 0:
        return '没有获取到动态!'
    data = data_json.get('data')
    cards = data.get('cards')
    dynamics = []
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
                d.full_text = card['item']['content']
            # 2:自己发表的动态
            elif d.dynamic_type == 2:
                c = json.loads(card['card'])
                d.full_text = c['item']['description']
            # 4:自己发表的无图片动态
            elif d.dynamic_type == 4:
                c = json.loads(card['card'])
                d.full_text = c['item']['content']
                pass
            # 8:视频投稿
            elif d.dynamic_type == 8:
                d.full_text = card['desc']
            # 512:动漫影剧
            elif d.dynamic_type == 512:
                pass
            # 4308:直播
            elif d.dynamic_type == 4308:
                pass
            # 64:专栏
            elif d.dynamic_type == 64:
                pass
            dynamics.append(d)
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
