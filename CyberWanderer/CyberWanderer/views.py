# 视图
from django.http import HttpResponse


def page_hello(request):
    html = '<h1>hello world!</h1>'
    return HttpResponse(html)
