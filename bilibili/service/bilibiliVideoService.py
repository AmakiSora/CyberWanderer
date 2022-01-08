"""
    b视频服务
"""
import datetime
import json
import logging

import requests

from CyberWanderer.utils import downloadUtils
from bilibili.models import BiliBiliVideo, BiliBiliUser

logger = logging.getLogger(__name__)


# 自动获取用户所有视频信息
def autoGetUserVideo(uid, to_db=True):
    has_more = 1
    page = 1
    while has_more == 1:
        data_json = getVideoInfo(uid, page)
        logger.info(data_json)
        has_more = analyzeUserVideo(data_json, to_db)
        page += 1
    oldCount, newCount = updateVideoCount(uid)
    return 'uid: ' + str(uid) + \
           ' 新增 ' + str(newCount - oldCount) + ' 条投稿信息!' + \
           ' 总共 ' + str(newCount) + ' 条投稿信息!'


# 获取视频信息
def getVideoInfo(uid, page):
    u = 'https://api.bilibili.com/x/space/arc/search'
    params = {
        'mid': uid,  # 用户id
        'ps': 50,  # 单次请求查询数(b站默认30,上限50)
        'pn': page,  # 页数(不填默认第一页)
    }
    data_json = requests.get(u, params)
    if data_json.status_code == 200:
        return json.loads(data_json.text)
    return None


# 解析json
def analyzeUserVideo(data_json, to_db):
    if data_json.get('code') != 0:
        return 0, '没有获取到视频信息!'
    data = data_json.get('data')
    vlist = data['list']['vlist']
    bvs = []
    bvNum = 0  # 记录视频数
    if vlist:
        for v in vlist:
            bv = BiliBiliVideo()
            bv.bvid = v['bvid']
            bv.name = v['author']
            bv.uid = v['mid']
            bv.created_time = datetime.datetime.fromtimestamp(v['created'])
            bv.title = v['title']
            bv.description = v['description']
            bv.pic = v['pic']
            bvs.append(bv)
            bvNum += 1
    logger.info('本次共获取 ' + str(bvNum) + '条视频信息')
    if to_db:
        BiliBiliVideo.objects.bulk_create(bvs, ignore_conflicts=True)  # 批量存入数据库(忽略重复id,即不会更新数据)
    else:
        for bv in bvs:
            logger.info(bv.bvid)
            logger.info(bv.uid)
            logger.info(bv.name)
            logger.info(bv.title)
            logger.info(bv.description)
            logger.info(bv.created_time)
            logger.info(bv.pic)
            logger.info('-------------------------------------------------------')
    count = data['page']['count']
    pageNum = data['page']['pn']
    pageSize = data['page']['ps']
    if pageSize * pageNum >= count:
        return 0
    return 1


# 更新投稿数
def updateVideoCount(uid):
    t = BiliBiliUser.objects.get(uid=uid)
    oldCount = t.video_count
    newCount = BiliBiliVideo.objects.filter(uid=uid).count()
    t.video_count = newCount
    t.save()
    return oldCount, newCount


# 下载视频(you-get)
def downloadVideo(bv, file_name, folder_name, proxy):
    url = 'https://www.bilibili.com/video/' + bv
    downloadUtils.download_file_local(url, file_name, folder_name, proxy)
