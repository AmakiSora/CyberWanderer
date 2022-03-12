'''
    推特请求服务
'''
import json

import requests

from CyberWanderer import settings
import logging

logger = logging.getLogger(__name__)
headers = {
    # "Host": "utils.com",
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
    # 'Accept': '*/*',
    # 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'x-guest-token': '',
    # 'x-utils-client-language': 'zh-cn',
    # 'x-utils-active-user': 'yes',
    # 'x-csrf-token': 'feb505674f40e6a83143c6ce4d1f4d04',
    # 'Sec-Fetch-Dest': 'empty',
    # 'Sec-Fetch-Mode': 'cors',
    # 'Sec-Fetch-Site': 'same-origin',
    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    # 'Referer': 'https://twitter.com/',
}

url_token = 'https://api.twitter.com/1.1/guest/activate.json'


# 获取token
def get_token():
    try:
        headers['x-guest-token'] = ''
        connect = requests.post(url_token, headers=headers, proxies=settings.PROXIES)
        logger.info(connect.text)
        token = json.loads(connect.text).get('guest_token', '')
        if token == '':
            raise IOError("请检查网络连接！")
        logger.info(str('成功获取到token：' + str(token)))
        headers['x-guest-token'] = token
        return token
    except IOError as e:
        logger.error("获取token出错!!!错误为: " + str(e))
        return "获取token出错!!!错误为: " + str(e)


i = 0


def get_headers():
    global i
    i += 1
    if i > 30:
        get_token()
        i = 0
    return headers
