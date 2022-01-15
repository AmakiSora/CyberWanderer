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
    # 更新多用户动态
    path('batchUpdateDynamic', batchUpdateDynamic),
    # 更新多用户信息
    path('batchUpdateBiliBiliUserInfo', batchUpdateBiliBiliUserInfo),
    # 下载视频至本地
    path('downloadVideo', downloadVideo),
    # path('',),
]
