# 视图
import json

from django.http import HttpResponse

from CyberWanderer.utils import downloadUtils


def page_hello(request):
    html = 'This is CyberWanderer V2.1.2'
    return HttpResponse(html)


# 通过you-get获取资源
def get_resource(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        url = body.get('url', None)
        if url is None:
            return HttpResponse("url不能为空！")
        file_name = body.get('file_name', None)
        folder_name = body.get('folder_name', None)
        proxy = body.get('proxy', False)
        return HttpResponse(downloadUtils.download_file_local(url, file_name, folder_name, proxy))
