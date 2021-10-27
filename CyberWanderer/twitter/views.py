from django.http import HttpResponse
from django.shortcuts import render
from .twitterService import *


def twitter_test(request):
    return HttpResponse('推特模块测试')


def analyzeUserInfo(request):
    # tweetsJson = getTweets("")
    # print(tweetsJson)
    # print(type(tweetsJson))

    return HttpResponse()
