"""
    百度翻译服务
"""

import requests
import random
from hashlib import md5
from CyberWanderer import settings
import logging

logger = logging.getLogger(__name__)
# 帐号/密码
appid = settings.BAIDU.get('appid')
appkey = settings.BAIDU.get('appkey')

# 请求地址
url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'


# 发送翻译请求(api)
def translate(text, target_language, original_language='auto'):
    target_language = target_converter(target_language)
    salt = random.randint(32768, 65536)
    sign = make_md5(appid + text + str(salt) + appkey)

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {
        'appid': appid,
        'q': text,
        'from': original_language,
        'to': target_language,
        'salt': salt,
        'sign': sign
    }
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    # print(json.dumps(result, indent=4, ensure_ascii=False))
    src, dst = analyze_translation(result)
    return dst


# 生成盐并签名
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


# 解析返回数据
def analyze_translation(data):
    if data.get('error_code'):
        logger.error(str('百度翻译出错->' + str(data)))
        return '', ''
    else:
        src = ''
        dst = ''
        rList = data.get('trans_result')
        if len(rList) == 1:
            src = rList[0].get('src')
            dst = rList[0].get('dst')
        else:
            for d in rList:
                src += d.get('src') + '\n'
                dst += d.get('dst') + '\n'
        return src, dst


# 转换器
def target_converter(target):
    if target == 'en':
        return 'en'
    elif target == 'zh':
        return 'zh'
    elif target == 'jp':
        return 'jp'
    elif target == 'fra':
        return 'fra'
    elif target == 'de':
        return 'de'
    elif target == 'ru':
        return 'ru'
    else:
        return target
