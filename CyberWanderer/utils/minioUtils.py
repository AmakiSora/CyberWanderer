"""
    MinIO 对象存储工具
"""
import io
import logging
import os

import requests
from minio import Minio

from CyberWanderer import settings
from CyberWanderer.utils.threadUtil import multithreading_list

logger = logging.getLogger(__name__)

minioClient = Minio(endpoint=settings.MINIO_ENDPOINT,
                    access_key=settings.MINIO_ACCESS_KEY,
                    secret_key=settings.MINIO_SECRET_KEY,
                    secure=False)


# 下载图片到对象存储(MinIO)
def upload_net_file_to_minio(url, file_name='', bucket_name='', useProxy=False):
    if file_name == '':
        file_name = url.split('/')[-1]
    # 校验文件是否已存在
    if minio_get_object_info(file_name, bucket_name) is not None:
        logger.info(str('资源已存在' + str(url)))
        return 'exist', None
    try:
        if useProxy:
            proxies = settings.PROXIES
        else:
            proxies = None
        r = requests.get(url, proxies=proxies)
        if r.status_code == 200:
            try:
                data = io.BytesIO(r.content)
                data_length = data.getbuffer().nbytes
                etag = minioClient.put_object(bucket_name=bucket_name,
                                              object_name=file_name,
                                              data=data,
                                              length=data_length)
                if etag:
                    logger.info(str("上传到MinIO成功,url:" + str(url)))
                    return 'success', None
                else:
                    logger.warning(str("上传到MinIO失败,url:" + str(url)))
                    return 'fail', None
            except Exception as e:
                logger.warning(e)
                logger.warning(str("上传到MinIO失败,url:" + str(url)))
                return 'fail', None
        else:
            logger.warning(str("资源已失效,url:" + str(url)))
            return 'notExist', None
    except:
        logger.error(str("连接失败!url:" + str(url)))
        return 'fail', None


# 获取单一资源信息(没有返回None)
def minio_get_object_info(object_name, bucket_name):
    try:
        return minioClient.stat_object(bucket_name, object_name)
    except:
        return None


# 本地文件上传到云
def upload_local_file_to_minio(local_url, bucket_name, file_name=''):
    if file_name == '':
        file_name = local_url.split('/')[-1]
    # 校验文件是否已存在
    if minio_get_object_info(file_name, bucket_name) is not None:
        logger.info(str('资源已存在,' + str(local_url)))
        return 'exist', None
    etag = minioClient.fput_object(bucket_name=bucket_name,
                                   object_name=file_name,
                                   file_path=local_url)
    if etag is None:
        logger.info(str('上传失败!url:' + str(local_url)))
        return 'fail', None
    logger.info('上传成功!url:' + local_url)
    return 'success', None


# 本地文件夹上传到云(多线程)
def upload_local_folder_to_minio(folder_name, bucket_name):
    # a代表所在根目录; b代表根目录下所有文件夹(以列表形式存在); c代表根目录下所有文件
    for a, b, c in os.walk(folder_name):
        urls = []
        for file_name in c:
            local_url = a + '/' + file_name
            urls.append(local_url)
        code, statusInfo = multithreading_list(urls, upload_local_file_to_minio, (bucket_name, ''))
        if code == 0:
            return "无文件上传!"
        elif code == 200:
            return '总共' + str(statusInfo.get('count', 0)) + '张图片!' + \
                   '已存在' + str(statusInfo.get('exist', 0)) + '张图片!' + \
                   '上传成功' + str(statusInfo.get('success', 0)) + '张图片!' + \
                   '上传失败' + str(statusInfo.get('fail', 0)) + '张图片!'

# upload_local_file_to_minio('C:/data/xxx', 'bucket_name')
# upload_local_folder_to_minio('C:/data', 'bucket_name')
