"""
    推特相关定时任务
"""
import datetime
import logging

from twitter.service import twitterRequestService, twitterUserService, searchTweetsService, userTweetsService

logger = logging.getLogger(__name__)


# 定时获取推文(搜索)
def batchUpdateTweetsByTask(params):
    twitterRequestService.get_token()
    # 筛选用户参数
    twitter_user_param = params.get('twitter_user_param', None)
    # 是否入库
    to_db = params.get('to_db', True)
    # 多线程
    threads = params.get('threads', True)
    # 搜索天数(默认7天)
    searchDay = params.get('searchDay', 7)
    logger.info('筛选用户参数: ' + str(twitter_user_param))
    # 根据user_param获取usernameList
    usernameList = twitterUserService.getUsernameListByUserParam(**twitter_user_param)
    if not usernameList:
        return
    now = datetime.datetime.today()
    since = (now - datetime.timedelta(searchDay)).strftime("%Y-%m-%d")
    until = now.strftime("%Y-%m-%d")
    logger.info('获取时间区间 : ' + since + ' 到 ' + until)
    intervalDays = 1
    resultList = []  # 返回信息列表
    for username in usernameList:
        if threads:  # 使用多线程
            searchTweetsService.auto_get_user_search_tweets_async(username, since, until, intervalDays)
        else:
            searchTweetsService.auto_get_user_search_tweets(username, since, until, to_db, intervalDays)
        oldCount, newCount = userTweetsService.updateTweetCount(username)
        result = '用户:' + username + '获取搜索推文成功!' + \
                 '新增 ' + str(newCount - oldCount) + ' 条,' + \
                 '现有 ' + str(newCount) + ' 条!\n'
        resultList.append(result)
    logger.info(str(resultList))
