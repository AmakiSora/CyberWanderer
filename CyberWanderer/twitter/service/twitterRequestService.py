'''
    推特请求服务
'''
import json

import requests

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
    # 'Connection': 'keep-alive',
}

url_token = 'https://api.twitter.com/1.1/guest/activate.json'


# 获取token
def get_token():
    token = json.loads(requests.post(url_token, headers=headers).text)['guest_token']
    print('guest—token：', token)
    headers['x-guest-token'] = token
    return token


def get_headers():
    if headers.get('x-guest-token') == '':
        get_token()
    return headers


# 初始化时获取
# try:
#     if headers.get('x-guest-token') == '':
#         get_token()
# except IOError:
#     print('未连接到推特!')
