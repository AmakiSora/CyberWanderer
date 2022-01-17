# 视图
import json

from django.http import HttpResponse

from CyberWanderer.utils import downloadUtils

import logging

logger = logging.getLogger(__name__)


def page_hello(request):
    html = 'This is CyberWanderer V2.0.9'
    logger.info("233")
    logger.error("233")
    logger.debug("233")
    logger.warning("233")
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
