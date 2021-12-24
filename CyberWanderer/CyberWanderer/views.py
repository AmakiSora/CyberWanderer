# 视图
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

def page_hello(request):
    html = 'This is CyberWanderer V1.9.1'
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')
    return HttpResponse(html)

