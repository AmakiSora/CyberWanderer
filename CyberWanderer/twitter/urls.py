from django.urls import path

from .views import *

urlpatterns = [
    # http://127.0.0.1:8000/twitter/
    path('changeToken', changeToken),  # 更换token

    path('analyzeUserTweets', analyzeUserTweets),  # 解析推文信息
    path('autoGetUserTweets', autoGetUserTweets),  # 自动获取推文

    path('analyzeUserInfo', analyzeUserInfo),  # 解析推特用户信息
    path('autoGetUserInfo', autoGetUserInfo),  # 自动获取用户信息

    path('autoGetUserSearchTweets', autoGetUserSearchTweets),  # 自动获取搜索推文

    path('autoGetUserImg', autoGetUserImg),  # 自动获取图片

    # path('',),
    # path('',),
    # path('',),
]
