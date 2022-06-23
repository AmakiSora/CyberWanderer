import json

from CyberWanderer.utils import responseUtils, downloadUtils
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
            return responseUtils.params_error('请传入uid参数!')
        to_db = body.get('to_db', True)  # 是否入库
        result = bilibiliUserService.autoGetUserInfo(uid, to_db)
        logger.info(result)
        return responseUtils.ok('获取用户信息成功', result)


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
                return responseUtils.params_error('请输入name或uid')
        result = bilibiliDynamicService.autoGetUserDynamic(uid, to_db, frequency)
        logger.info(result)
        return responseUtils.ok('获取用户动态成功', result)


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
                return responseUtils.params_error('请输入name或uid')
        result = bilibiliVideoService.autoGetUserVideo(uid, to_db)
        logger.info(result)
        return responseUtils.ok('获取所有视频信息成功', result)


# 自动获取图片
def autoGetImg(request):
    if request.method == 'POST':
        body = json.loads(request.body)

        # 获取图片范围
        filter_obj = body.get('dynamic_param', None)
        if filter_obj is None:
            return responseUtils.params_error("filter_obj不能为空！")

        # 下载方式
        download_method = body.get('download_method', None)
        # 默认上传到七牛云
        if download_method is None:
            download_method = {'method': 'qiniu',
                               'bucket_name': 'default-0'}

        urls = bilibiliImgDownloadService.get_img_url(**filter_obj)
        result = downloadUtils.auto_get_img(urls, download_method)

        logger.info(result)
        return responseUtils.ok('获取图片成功', result)


# 更新多用户动态
def batchUpdateDynamic(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        usernameList = body.get('usernameList', None)
        to_db = body.get('to_db', True)  # 是否入库
        frequency = body.get('frequency', 20)  # 循环次数
        threads = body.get('threads', False)  # 多线程
        if usernameList is None:
            return responseUtils.params_error("名单列表不能为空！")
        elif type(usernameList) is not list:
            return responseUtils.params_error("参数需要为列表！")
        logger.info(usernameList)
        if threads:
            result = bilibiliDynamicService.batchUpdateDynamicThreads(usernameList, to_db, frequency)
            logger.info(result)
            return responseUtils.ok('更新多用户动态成功', result)
        else:
            return responseUtils.params_error('现在只有多线程处理方式！')


# 批量更新用户信息
def batchUpdateBiliBiliUserInfo(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        filter_obj = body.get('bilibili_user_param', None)
        if filter_obj is None:
            return responseUtils.params_error("bilibili_user_param不能为空！")
        result = bilibiliUserService.updateBiliBiliUserInfo(**filter_obj)
        logger.info(result)
        return responseUtils.ok('批量更新用户信息成功', result)


# 下载b站视频
def downloadVideo(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        bv = body.get('bv', None)
        if bv is None:
            return responseUtils.params_error("bv不能为空！")
        file_name = body.get('file_name', None)
        folder_name = body.get('folder_name', None)
        proxy = body.get('proxy', False)
        result = bilibiliVideoService.downloadVideo(bv, file_name, folder_name, proxy)
        logger.info(result)
        return responseUtils.ok(result)
