"""
    翻译狗翻译服务
"""

# 请求地址
import requests

url = 'http://www.fanyigou.com/sdoc/text/trans'


# 发送翻译请求
def translate(text, target_language, original_language='auto'):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    payload = {
        'deviceId': '42cc5272d9c7e2',
        'src': text,
        'from': original_language,
        'to': target_language,
        'deviceType': 'web'
    }
    r = requests.post(url, data=payload, headers=headers)
    result = r.json()
    # print(json.dumps(result, indent=4, ensure_ascii=False))
    dst = analyze_translation(result)
    return dst


# 解析返回数据
def analyze_translation(data):
    if data.get('code') != 0:
        print('翻译狗翻译出错->', data)
        return ''
    dst = data.get('data').get('dst')
    return dst
