import json

from django.http import HttpResponse


# 翻译语句
from translate.models import Translation


def translate(request):
    print(233)
    if request.method == 'POST':
        body = json.loads(request.body)
        original_language = body.get('original_language', 'auto')
        target_language = body.get('target_language', None)
        if target_language is None:
            return HttpResponse("目标语言不能为空！", content_type="application/json")
        Translation.objects.create(original_text=233)
        return HttpResponse("data", content_type="application/json")
