"""
    翻译服务
"""
from translate.models import Translation
from translate.service import baiduTranslateService, fanyigouTranslateService, youdaoTranslateService, \
    tencentTranslateService, deepLTranslateService, googleTranslateService


def getTranslate(text, select_engine, target_language, original_language='auto', to_db=True):
    result_translation = {}
    target_language = target_converter(target_language)
    if not select_engine:
        print('全部调用!')
        result_translation['baidu_translation'] = baiduTranslateService.translate(text, target_language,
                                                                                  original_language)
        result_translation['fanyigou_translation'] = fanyigouTranslateService.translate(text, target_language,
                                                                                        original_language)
        result_translation['youdao_translation'] = youdaoTranslateService.translate(text, target_language,
                                                                                    original_language)
        result_translation['tencent_translation'] = tencentTranslateService.translate(text, target_language,
                                                                                      original_language)
        result_translation['deepL_translation'] = deepLTranslateService.translate(text, target_language,
                                                                                  original_language)
        result_translation['google_translation'] = googleTranslateService.translate(text, target_language,
                                                                                    original_language)

    if select_engine.find('baidu') != -1:
        print('百度翻译!')
        result_translation['baidu_translation'] = baiduTranslateService.translate(text, target_language,
                                                                                  original_language)

    if select_engine.find('fanyigou') != -1:
        print('翻译狗翻译!')
        result_translation['fanyigou_translation'] = fanyigouTranslateService.translate(text, target_language,
                                                                                        original_language)

    if select_engine.find('youdao') != -1:
        print('有道翻译!')
        result_translation['youdao_translation'] = youdaoTranslateService.translate(text, target_language,
                                                                                    original_language)

    if select_engine.find('tencent') != -1:
        print('腾讯翻译!')
        result_translation['tencent_translation'] = tencentTranslateService.translate(text, target_language,
                                                                                      original_language)

    if select_engine.find('DeepL') != -1:
        print('DeepL翻译!')
        result_translation['deepL_translation'] = deepLTranslateService.translate(text, target_language,
                                                                                  original_language)

    if select_engine.find('google') != -1:
        print('google翻译!')
        result_translation['google_translation'] = googleTranslateService.translate(text, target_language,
                                                                                    original_language)

    if to_db:
        Translation.objects.create(
            original_language=original_language,
            target_language=target_language,
            original_text=text,
            baidu_translation=result_translation.get('baidu_translation', ''),
            fanyigou_translation=result_translation.get('fanyigou_translation', ''),
            youdao_translation=result_translation.get('youdao_translation', ''),
            tencent_translation=result_translation.get('tencent_translation', ''),
            deepL_translation=result_translation.get('deepL_translation', ''),
            google_translation=result_translation.get('google_translation', '')
        )
    else:
        print('original_text:' + text)
        for d in result_translation.keys():
            print(d + ':' + result_translation.get(d))
    result_translation['original_text:'] = text
    return result_translation


# 目标语言转换器
def target_converter(target):
    if target in ['en', 'EN', 'english', 'English', '英文', '英', '英语']:
        return 'en'
    elif target in ['zh', 'ZH', 'chinese', 'Chinese', '简体中文', '中文', '中', '汉语']:
        return 'zh'
    elif target in ['jp', 'JP', 'ja', 'JA', 'japanese', 'Japanese', '日语', '日']:
        return 'jp'
    elif target in ['fr', 'fra', 'FRA', 'french', 'French', '法语', '法']:
        return 'fra'
    elif target in ['de', 'DE', 'german', 'German', '德语', '德']:
        return 'de'
    elif target in ['ru', 'RU', 'russian', 'Russian', '俄语', '俄']:
        return 'ru'
    else:
        return target
