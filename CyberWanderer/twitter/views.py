import datetime
import json

from django.http import HttpResponse
from .service import twitterUserService, userTweetsService, twitterRequestService, searchTweetsService, \
    userImgDownloadService, showTweetsService


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
        userTweetsService.autoGetUserTweets(rest_id, count, to_db, frequency, updateTweet)
        userTweetsService.updateTweetCount(username)
        return HttpResponse('自动获取用户推文成功!')


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
        twitterUserService.autoGetUserInfo(username, to_db)
        return HttpResponse('自动获取推特用户信息成功!')


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
        starttime = datetime.datetime.now()
        searchTweetsService.auto_get_user_search_tweets(username, since, until, to_db, intervalDays)
        endtime = datetime.datetime.now()
        userTweetsService.updateTweetCount(username)
        time = (endtime - starttime).seconds
        return HttpResponse('自动获取搜索推文信息成功!耗时:' + str(time) + "s")


# 自动获取图片
def autoGetUserImg(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        folder_name = body.get('folder_name', '')
        filter_obj = body.get('tweets_param', None)
        if filter_obj is None:
            return HttpResponse("filter_obj不能为空！")
        return HttpResponse(userImgDownloadService.auto_get_user_img(folder_name, **filter_obj))


# 展示推文数据
def showTweets(request):
    print(request.GET.items())
    params = {'username': request.GET.get('username')}
    data = showTweetsService.show_user_tweets(**params)
    return HttpResponse(data, content_type="application/json")
