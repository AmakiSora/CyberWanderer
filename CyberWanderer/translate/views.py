import json

from django.http import HttpResponse

# 翻译语句
from translate.models import Translation
from translate.service import translateService


def translate(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        text = body.get('text', None)
        if not text:
            return HttpResponse("请填写需要翻译的语句！", content_type="application/json")
        target_language = body.get('target_language', 'zh')
        original_language = body.get('original_language', 'auto')
        select_engine = body.get('select_engine', None)
        to_db = body.get('to_db', True)
        if target_language is None:
            return HttpResponse("目标语言不能为空！", content_type="application/json")
        result = translateService.getTranslate(
            text=text,
            select_engine=select_engine,
            target_language=target_language,
            original_language=original_language,
            to_db=to_db
        )
        return HttpResponse(json.dumps(result), content_type="application/json")
