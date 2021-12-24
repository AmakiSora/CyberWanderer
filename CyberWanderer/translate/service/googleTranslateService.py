"""
    谷歌翻译服务
    需代理
"""

import goslate
import urllib.request
from CyberWanderer import settings
import logging

logger = logging.getLogger(__name__)

# 发送翻译请求
def translate(text, target_language, original_language='auto'):
    target_language = target_converter(target_language)
    proxy_handler = urllib.request.ProxyHandler(settings.PROXIES)
    proxy_opener = urllib.request.build_opener(proxy_handler)
    gs = goslate.Goslate(opener=proxy_opener)
    try:
        dst = gs.translate(text, target_language)
    except:
        logger.error('谷歌翻译出错')
        dst = ''
    return dst


# 转换器
def target_converter(target):
    if target == 'en':
        return 'en'
    elif target == 'zh':
        return 'zh-CN'
    elif target == 'jp':
        return 'ja'
    elif target == 'fra':
        return 'fr'
    elif target == 'de':
        return 'de'
    elif target == 'ru':
        return 'ru'
    else:
        return target
