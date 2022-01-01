# 视图
from django.http import HttpResponse


def page_hello(request):
    html = 'This is CyberWanderer V1.9.8'
    return HttpResponse(html)

