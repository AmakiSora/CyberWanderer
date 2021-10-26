from django.http import HttpResponse
from django.shortcuts import render


def twitter_test(request):
    return HttpResponse('推特模块测试')
