# 视图
from django.http import HttpResponse


def page_hello(request):
    html = 'This is CyberWanderer V2.0.1'
    return HttpResponse(html)

