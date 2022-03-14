import json

# 翻译语句
from CyberWanderer.utils import responseUtils
from translate.service import translateService


def translate(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        text = body.get('text', None)
        if not text:
            return responseUtils.params_error("请填写需要翻译的语句！")
        target_language = body.get('target_language', 'zh')
        original_language = body.get('original_language', 'auto')
        select_engine = body.get('select_engine', None)
        to_db = body.get('to_db', True)
        if target_language is None:
            return responseUtils.params_error("目标语言不能为空！")
        result = translateService.getTranslate(
            text=text,
            select_engine=select_engine,
            target_language=target_language,
            original_language=original_language,
            to_db=to_db
        )
        return responseUtils.ok('', json.dumps(result))
