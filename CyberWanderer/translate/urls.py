from django.urls import path

from .views import *

urlpatterns = [
    # http://127.0.0.1:8000/translate/
    # 翻译语句
    path('translate', translate),
    #
    # path('',),
]
