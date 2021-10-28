from django.http import HttpResponse
from .service import twitterUserService, tweetsService, twitterRequestService


def analyzeUserTweets(request):
    return HttpResponse()


def autoGetUserTweets(request, username):
    rest_id = twitterUserService.getRestIdByUsername(username)
    t = tweetsService.autoGetUserTweets(rest_id, 20, True)
    return HttpResponse(t)


def analyzeUserInfo(request):
    return HttpResponse()


def autoGetUserInfo(request, username):
    return HttpResponse(twitterUserService.autoGetUserInfo(username, True))


def changeToken(request):
    return HttpResponse(twitterRequestService.get_token())


def test233(request):
    print(request.body)
    print(request.GET)
    print(request.POST)
    print(request.method)
    return HttpResponse('2333')
