import json

from django.http import HttpResponse
from .service import twitterUserService, userTweetsService, twitterRequestService


def analyzeUserTweets(request):
    return HttpResponse()


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
        print(updateTweet)
        userTweetsService.autoGetUserTweets(rest_id, count, to_db, frequency, updateTweet)
        return HttpResponse('自动获取用户推文成功!')


def analyzeUserInfo(request):
    return HttpResponse()


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


def changeToken(request):
    return HttpResponse(twitterRequestService.get_token())


def test233(request):
    print(request.body)
    print(request.GET)
    print(request.POST)
    print(request.method)
    return HttpResponse('2333')
