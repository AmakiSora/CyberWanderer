import datetime
import json

from django.http import HttpResponse
from .service import twitterUserService, userTweetsService, twitterRequestService, searchTweetsService, \
    twitterDownloadService, showTweetsService
import logging

logger = logging.getLogger(__name__)


# 更换token
def changeToken(request):
    return HttpResponse(twitterRequestService.get_token())


# 解析推文信息
def analyzeUserTweets(request):
    return HttpResponse('暂时不开放此功能')


# 自动获取推文
def autoGetUserTweets(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        username = body.get('username')
        if username is None:
            return HttpResponse('请传入username参数!')
        if username == '':
            return HttpResponse('username不能为空!')
        count = body.get('count', 20)  # 每次请求获取的推文数
        to_db = body.get('to_db', True)  # 是否入库
        frequency = body.get('frequency', 1)  # 循环次数
        rest_id = twitterUserService.getRestIdByUsername(username)
        if rest_id is None:
            return HttpResponse('用户在数据库中不存在!')
        updateTweet = body.get('updateTweet', False)  # 是否更新
        re = userTweetsService.autoGetUserTweets(rest_id, count, to_db, frequency, updateTweet)
        userTweetsService.updateTweetCount(username)
        return HttpResponse(re)


# 解析推特用户信息
def analyzeUserInfo(request):
    return HttpResponse('暂时不开放此功能')


# 自动获取用户信息
def autoGetUserInfo(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        username = body.get('username')
        if username is None:
            return HttpResponse('请传入username参数!')
        if username == '':
            return HttpResponse('username不能为空!')
        to_db = body.get('to_db', True)  # 是否入库
        re = twitterUserService.autoGetUserInfo(username, to_db)
        return HttpResponse(re)


# 自动获取搜索推文
def autoGetUserSearchTweets(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        username = body.get('username')
        if username is None:
            return HttpResponse('请传入username参数!')
        if username == '':
            return HttpResponse('username不能为空!')
        to_db = body.get('to_db', True)  # 是否入库
        since = body.get('since')  # 起始时间
        until = body.get('until')  # 截止时间
        if since is None or until is None:
            return HttpResponse('起始或截止不能为空!')
        intervalDays = body.get('intervalDays')  # 截止时间
        coroutine = body.get('coroutine', False)  # 是否启用协程
        starttime = datetime.datetime.now()
        # searchTweetsService.auto_get_user_search_tweets(username, since, until, to_db, intervalDays)
        if coroutine is True:
            searchTweetsService.auto_get_user_search_tweets_coroutine(username, since, until, to_db, intervalDays)
        else:
            searchTweetsService.auto_get_user_search_tweets(username, since, until, to_db, intervalDays)
        endtime = datetime.datetime.now()
        oldCount, newCount = userTweetsService.updateTweetCount(username)
        time = (endtime - starttime).seconds
        return HttpResponse('自动获取推文成功!耗时:' + str(time) + 's,' +
                            '新增了 ' + str(newCount - oldCount) + ' 条推文,' +
                            '现有推文 ' + str(newCount) + ' 条!')


# 自动获取图片
def autoGetImg(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        filter_obj = body.get('tweets_param', None)
        if filter_obj is None:
            return HttpResponse("filter_obj不能为空！")
        return HttpResponse(twitterDownloadService.auto_get_img(**filter_obj))


# 展示推文数据
def showTweets(request):
    logger.info(request.GET.items())
    params = {'username': request.GET.get('username')}
    data = showTweetsService.show_user_tweets(**params)
    return HttpResponse(data, content_type="application/json")


# 更新多用户推文
def batchUpdateTweets(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        usernameList = body.get('usernameList', None)
        count = body.get('count', 200)  # 每次请求获取的推文数
        to_db = body.get('to_db', True)  # 是否入库
        updateTweet = body.get('updateTweet', False)  # 是否更新
        frequency = body.get('frequency', 20)  # 循环次数
        threads = body.get('threads', False)  # 多线程
        if usernameList is None:
            return HttpResponse("名单列表不能为空！")
        elif type(usernameList) is not list:
            return HttpResponse("参数需要为列表！")
        logger.info(usernameList)
        if threads:
            return HttpResponse(
                userTweetsService.batchUpdateTweetsThreads(usernameList, count, to_db, frequency, updateTweet))
        else:
            return HttpResponse(userTweetsService.batchUpdateTweets(usernameList, count, to_db, frequency, updateTweet))


# 批量更新用户信息
def batchUpdateTwitterUserInfo(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        filter_obj = body.get('twitter_user_param', None)
        if filter_obj is None:
            return HttpResponse("twitter_user_param不能为空！")
        return HttpResponse(twitterUserService.updateTwitterUserInfo(**filter_obj))


# 下载推文视频
def downloadVideo(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        id = body.get('id', None)
        if id is None:
            return HttpResponse("id不能为空！")
        file_name = body.get('file_name', None)
        folder_name = body.get('folder_name', None)
        proxy = body.get('proxy', False)
        return HttpResponse(twitterDownloadService.downloadVideo(id, file_name, folder_name, proxy))
