# 视图
from django.http import HttpResponse
# from .utils import twitterService


def page_hello(request):
    html = 'This is CyberWanderer V1.8.6'
    return HttpResponse(html)


def connection(request):
    url = 'baidu.com'
    # data = twitterService.getTweets(url)
    return HttpResponse()

# def page_test(request, username):
#     return HttpResponse(username)
