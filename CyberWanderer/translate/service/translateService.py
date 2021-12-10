"""
    翻译服务
"""
from translate.models import Translation
from translate.service import baiduTranslateService, fanyigouTranslateService


def getTranslate(text, select_engine, target_language, original_language='auto', to_db=True):
    result_translation = {}
    if not select_engine:
        print('全部调用!')
        result_translation['baidu_translation'] = baiduTranslateService.translate(text, target_language, original_language)
        result_translation['fanyigou_translation'] = fanyigouTranslateService.translate(text, target_language, original_language)
    if select_engine.find('baidu') != -1:
        print('百度翻译!')
        result_translation['baidu_translation'] = baiduTranslateService.translate(text, target_language, original_language)
    if select_engine.find('fanyigou') != -1:
        result_translation['fanyigou_translation'] = fanyigouTranslateService.translate(text, target_language, original_language)

    if to_db:
        Translation.objects.create(
            original_language=original_language,
            target_language=target_language,
            original_text=text,
            baidu_translation=result_translation.get('baidu_translation', ''),
            fanyigou_translation=result_translation.get('fanyigou_translation',''),
            youdao_translation=result_translation.get('youdao_translation', ''),
            deepL_translation=result_translation.get('deepL_translation', ''),
            google_translation=result_translation.get('google_translation', '')
        )
    else:
        print('original_text:' + text)
        for d in result_translation.keys():
            print(d + ':' + result_translation.get(d))
    result_translation['original_text:'] = text
    return result_translation
