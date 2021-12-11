"""
    有道翻译服务
"""
# 请求地址
import requests

url = 'https://aidemo.youdao.com/trans'


# 发送翻译请求
def translate(text, target_language, original_language='auto'):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    payload = {
        'q': text,
        'from': original_language,
        'to': target_language,
    }
    r = requests.post(url, data=payload, headers=headers)
    result = r.json()
    # print(json.dumps(result, indent=4, ensure_ascii=False))
    src, dst = analyze_translation(result)
    return dst


# 解析返回数据
def analyze_translation(data):
    if data.get('errorCode') != '0':
        print('有道翻译出错->', data)
        return '', ''
    src = data.get('query', '')
    dst = ''
    for d in data.get('translation'):
        dst += d
    return src, dst
