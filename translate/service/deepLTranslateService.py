"""
    DeepL翻译服务
    限制得比较死,少用
"""

# 请求地址
import json
import time

import requests

from CyberWanderer import settings
import logging

logger = logging.getLogger(__name__)
url = 'https://www2.deepl.com/jsonrpc?method=LMT_handle_jobs'


# 发送翻译请求
def translate(text, target_language, original_language='auto'):
    target_language = target_converter(target_language)
    headers = {'Content-Type': 'application/json'}
    payload = {
        'method': 'LMT_handle_jobs',
        'id': 23333,
        'params': {
            "jobs": [
                {
                    "kind": "default",
                    "raw_en_sentence": text,
                    "preferred_num_beams": 1
                }
            ],
            "lang": {
                "preference": {
                    "weight": {},
                    "default": "default"
                },
                "source_lang_user_selected": original_language,
                "target_lang": target_language
            },
            "timestamp": time.time()
        }
    }
    r = requests.post(url, json=payload, headers=headers)

    result = r.json()
    # print(json.dumps(result, indent=4, ensure_ascii=False))
    dst = analyze_translation(result)
    return dst


# 解析返回数据
def analyze_translation(data):
    if err := data.get('error'):
        logger.error(str('DeepL翻译出错->' + str(err)))
        return ''
    dst = data.get('result').get('translations')[0].get('beams')[0].get('postprocessed_sentence')
    return dst


# 转换器
def target_converter(target):
    if target == 'en':
        return 'EN'
    elif target == 'zh':
        return 'ZH'
    elif target == 'jp':
        return 'JA'
    elif target == 'fra':
        return 'FR'
    elif target == 'de':
        return 'DE'
    elif target == 'ru':
        return 'RU'
    else:
        return target
