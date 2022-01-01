from django.urls import path

from .views import *

urlpatterns = [
    # http://127.0.0.1:8000/bilibili/
    # 自动获取用户信息
    path('autoGetUserInfo', autoGetUserInfo),
    # 自动获取用户动态
    path('autoGetUserDynamic', autoGetUserDynamic),
    # 自动获取用户所有视频信息
    path('autoGetUserVideo', autoGetUserVideo),
    # 自动获取图片
    path('autoGetImg', autoGetImg),
    # path('',),
]
