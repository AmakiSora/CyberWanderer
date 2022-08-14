"""
    获取推文定时任务
"""
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore

from CyberWanderer import settings

logger = logging.getLogger(__name__)

# 实例化调度器
scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
# 调度器使用DjangoJobStore()
scheduler.add_jobstore(DjangoJobStore(), "default")
# 默认在启动时开启
scheduler.start()


# 新增任务(样例)
def add(job_id, cron, params):
    scheduler.add_job(
        example_function,
        trigger=CronTrigger(**cron),
        id=job_id,
        max_instances=1,
        replace_existing=True,
        kwargs=params
    )
    logger.info("新增定时任务,id:" + job_id + " ,cron:" + cron + " ,params" + params)


# 移除任务(指定)
def remove(job_id):
    scheduler.remove_job(job_id)
    logger.info("移除定时任务!,id:" + job_id)


# 移除任务(所有)
def remove_all():
    scheduler.remove_all_jobs()
    logger.info("移除所有定时任务!")


# 开启任务(总开关)
def start():
    scheduler.start(paused=True)
    logger.info("开启定时任务!")


# 暂停任务(指定)
def pause(job_id):
    scheduler.pause_job(job_id)
    logger.info("暂停定时任务!,id:" + job_id)


# 暂停任务(所有)
def pause_all():
    scheduler.pause()
    logger.info("暂停所有定时任务!")


# 恢复任务(指定)
def resume(job_id):
    scheduler.resume_job(job_id)
    logger.info("恢复定时任务!,id:" + job_id)


# 恢复任务(所有)
def resume_all():
    scheduler.resume()
    logger.info("恢复所有定时任务!")


# 修改任务(指定)
def modify(job_id, cron, params):
    scheduler.modify_job(job_id, trigger=CronTrigger(**cron), kwargs=params)
    logger.info("修改定时任务!,id:" + job_id + " ,cron:" + str(cron) + " ,params:" + str(params))


# 查询任务(所有)
def query():
    jobs = scheduler.get_jobs()
    logger.info(jobs)
    return jobs


# 示例任务
def example_function(param):
    logger.info("定时任务样例!")
    logger.info(param)
