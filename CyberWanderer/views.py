# 视图
import json
import logging

from django.http import HttpResponse

from CyberWanderer.task import APSchedulerTask
from CyberWanderer.utils import downloadUtils, responseUtils, qiniuUtils

logger = logging.getLogger(__name__)


def page_hello(request):
    html = 'This is CyberWanderer V2.2.6'
    return HttpResponse(html)


# 通过you-get获取资源
def get_resource(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        url = body.get('url', None)
        if url is None:
            return responseUtils.params_error("url不能为空！")
        file_name = body.get('file_name', None)
        folder_name = body.get('folder_name', None)
        proxy = body.get('proxy', False)
        return responseUtils.ok(downloadUtils.download_file_local(url, file_name, folder_name, proxy))


# 全量下载七牛云文件
def download_all_from_qiniu(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        # 资源池
        bucket_name = body.get('bucket_name', None)
        # 目标文件夹
        folder_name = body.get('folder_name', None)
        # url前缀,默认http://img.icarus-alpha.cn/
        url_prefix = body.get('url_prefix', 'http://img.icarus-alpha.cn/')
        # 偏移标记
        marker = body.get('marker', None)
        # 全量下载
        while True:
            # 获取
            urls, marker = qiniuUtils.qiniu_get_all_info(bucket_name=bucket_name, marker=marker, url_prefix=url_prefix)
            download_method = {'method': 'local',
                               'local_url': folder_name}
            result_msg = downloadUtils.auto_get_img(urls, download_method)
            logger.info(result_msg)
            if not marker:
                break
    return responseUtils.ok("下载完毕")


'''
    定时任务
'''


# 新增任务(样例)
def task_add(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        # 任务id
        job_id = body.get('job_id', None)
        # 执行时间
        cron = body.get('cron', None)
        # 任务自定义参数
        params = body.get('params', None)
        APSchedulerTask.add(job_id, cron, params)
        return responseUtils.ok('新增定时任务 ' + job_id + ' 成功!')


# 移除任务(指定)
def task_remove(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        job_id = body.get('job_id', None)
        APSchedulerTask.remove(job_id)
        return responseUtils.ok('定时任务 ' + job_id + ' 移除成功!')


# 移除任务(所有)
def task_remove_all(request):
    APSchedulerTask.remove_all()
    return responseUtils.ok('所有定时任务移除成功!')


# 开启任务(总开关)
def task_start(request):
    APSchedulerTask.start()
    return responseUtils.ok('定时任务开启成功!')


# 暂停任务(指定)
def task_pause(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        job_id = body.get('job_id', None)
        APSchedulerTask.pause(job_id)
        return responseUtils.ok('定时任务暂停成功!')


# 暂停任务(所有)
def task_pause_all(request):
    APSchedulerTask.pause_all()
    return responseUtils.ok('所有定时任务暂停成功!')


# 恢复任务(指定)
def task_resume(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        job_id = body.get('job_id', None)
        APSchedulerTask.resume(job_id)
        return responseUtils.ok('定时任务 ' + job_id + ' 恢复成功!')


# 恢复任务(所有)
def task_resume_all(request):
    APSchedulerTask.resume_all()
    return responseUtils.ok('所有定时任务恢复成功!')


# 修改任务(指定)
def task_modify(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        # 任务id
        job_id = body.get('job_id', None)
        # 执行时间
        cron = body.get('cron', None)
        # 任务自定义参数
        params = body.get('params', None)
        APSchedulerTask.modify(job_id, cron, params)
        return responseUtils.ok('修改定时任务 ' + job_id + ' 成功!')


# 查询任务(所有)
def task_query(request):
    result = []
    for i in APSchedulerTask.query():
        result.append(i.__getstate__().__str__())
    return responseUtils.ok('定时任务', result)
