# 视图
import json
import logging

from django.http import HttpResponse

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

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

# 开启定时工作
try:
    # 1.实例化调度器
    scheduler = BackgroundScheduler()

    # 2.调度器使用DjangoJobStore()
    scheduler.add_jobstore(DjangoJobStore(), "default")


    # 3.设置定时任务，选择方式为interval，时间间隔为10s
    #     # 另一种方式为每天固定时间执行任务，对应代码为：
    #     # @register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10',id='task_time')
    #
    @register_job(scheduler, "interval", seconds=10, replace_existing=True )
    def my_job():
        # 这里写你要执行的任务
        logger.info("定时任务测试!!!")


    # 4.注册定时任务
    # register_events(scheduler)

    # 5.开启定时任务
    scheduler.start()

except Exception as e:
    print(e)
    # 有错误就停止定时器
    scheduler.shutdown()


