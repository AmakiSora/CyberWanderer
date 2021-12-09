import uuid

from django.db import models


# 翻译
class Translation(models.Model):
    translation_id = models.UUIDField("翻译id", primary_key=True, auto_created=True, default=uuid.uuid4())
    from_id = models.CharField('来源id', max_length=255, default='')
    translate_time = models.DateTimeField("翻译时间", auto_now=True)
    original_language = models.CharField('原文语言', max_length=255, default='')
    target_language = models.CharField('目标语言', max_length=255, default='')

    original_text = models.TextField('原文', default='')
    baidu_translation = models.TextField('百度翻译', default='')
    youdao_translation = models.TextField('有道翻译', default='')
    deepL_translation = models.TextField('DeepL翻译', default='')
    google_translation = models.TextField('Google翻译', default='')
