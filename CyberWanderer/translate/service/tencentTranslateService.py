"""
    腾讯翻译服务
"""
import hashlib
import hmac
import json
import time
from datetime import datetime

import requests

from CyberWanderer import settings

# 密钥参数
secret_id = settings.TENCENT.get('secret_id')
secret_key = settings.TENCENT.get('secret_key')

# 请求地址
url = 'https://tmt.tencentcloudapi.com'


# 发送翻译请求(api)
def translate(text, target_language, original_language='auto'):
    target_language = target_converter(target_language)
    payload = {
        'ProjectId': 233,
        'SourceText': text,
        'Source': original_language,
        'Target': target_language
    }
    headers = getHeaders(payload)
    r = requests.post(url, json=payload, headers=headers)
    result = r.json()
    # print(json.dumps(result, indent=4, ensure_ascii=False))
    dst = analyze_translation(result)
    return dst


# 解析返回数据
def analyze_translation(data):
    if err := data.get('Response').get('Error'):
        print('腾讯翻译出错->', err)
        return ''
    return data.get('Response').get('TargetText')


# 获取headers(傻逼腾讯,搞这么复杂)
def getHeaders(payload):
    service = "tmt"
    host = "tmt.tencentcloudapi.com"
    algorithm = "TC3-HMAC-SHA256"
    timestamp = int(time.time())
    # print(timestamp)
    date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
    params = payload

    # ************* 步骤 1：拼接规范请求串 *************
    http_request_method = "POST"
    canonical_uri = "/"
    canonical_querystring = ""
    ct = "application/json"
    payload = json.dumps(params)
    canonical_headers = "content-type:%s\nhost:%s\n" % (ct, host)
    signed_headers = "content-type;host"
    hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    canonical_request = (http_request_method + "\n" +
                         canonical_uri + "\n" +
                         canonical_querystring + "\n" +
                         canonical_headers + "\n" +
                         signed_headers + "\n" +
                         hashed_request_payload)
    # print(canonical_request)

    # ************* 步骤 2：拼接待签名字符串 *************
    credential_scope = date + "/" + service + "/" + "tc3_request"
    hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    string_to_sign = (algorithm + "\n" +
                      str(timestamp) + "\n" +
                      credential_scope + "\n" +
                      hashed_canonical_request)

    # print(string_to_sign)

    # ************* 步骤 3：计算签名 *************
    # 计算签名摘要函数
    def sign(key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    secret_date = sign(("TC3" + secret_key).encode("utf-8"), date)
    secret_service = sign(secret_date, service)
    secret_signing = sign(secret_service, "tc3_request")
    signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
    # print(signature)

    # ************* 步骤 4：拼接 Authorization *************
    authorization = (algorithm + " " +
                     "Credential=" + secret_id + "/" + credential_scope + ", " +
                     "SignedHeaders=" + signed_headers + ", " +
                     "Signature=" + signature)
    # print(authorization)
    headers = {
        'Authorization': authorization,
        'Content-Type': 'application/json',
        'X-TC-Action': 'TextTranslate',
        'X-TC-Version': '2018-03-21',
        'X-TC-Region': 'ap-shanghai',
        'X-TC-Timestamp': str(timestamp),
        'X-TC-Language': 'zh-CN',
    }
    return headers


# 转换器
def target_converter(target):
    if target == 'en':
        return 'en'
    elif target == 'zh':
        return 'zh'
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
