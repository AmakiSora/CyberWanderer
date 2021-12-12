"""
    谷歌翻译服务
    需代理
"""

import goslate
import urllib.request
from CyberWanderer import settings


# 发送翻译请求
def translate(text, target_language, original_language='auto'):
    proxy_handler = urllib.request.ProxyHandler(settings.PROXIES)
    proxy_opener = urllib.request.build_opener(proxy_handler)
    gs = goslate.Goslate(opener=proxy_opener)
    try:
        dst = gs.translate(text, target_language)
    except:
        print('谷歌翻译出错')
        dst = ''
    return dst
