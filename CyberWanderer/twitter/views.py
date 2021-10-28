from django.http import HttpResponse
from .service import twitterUserService, tweetsService, twitterRequestService


def analyzeUserTweets(request):
    return HttpResponse()


def autoGetUserTweets(request, username):
    rest_id = twitterUserService.getUserIdByUsername(username)
    t = tweetsService.autoGetUserTweets(rest_id, 20, True)
    return HttpResponse(t)


def analyzeUserInfo(request):
    return HttpResponse()


def autoGetUserInfo(request):
    return HttpResponse()


def changeToken(request):
    return HttpResponse(twitterRequestService.get_token())
