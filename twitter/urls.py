from django.urls import path

from .views import *

urlpatterns = [
    # http://127.0.0.1:8000/twitter/
    # 更换token
    path('changeToken', changeToken),
    # 解析推文信息
    # path('analyzeUserTweets', analyzeUserTweets),
    # 自动获取推文
    path('autoGetUserTweets', autoGetUserTweets),
    # 解析推特用户信息
    # path('analyzeUserInfo', analyzeUserInfo),
    # 自动获取用户信息
    path('autoGetUserInfo', autoGetUserInfo),
    # 自动获取搜索推文
    path('autoGetUserSearchTweets', autoGetUserSearchTweets),
    # 自动获取图片
    path('autoGetImg', autoGetImg),
    # 自动获取图片(定时任务)
    path('autoGetImgByTask', autoGetImgByTask),
    # 展示推文数据
    path('showTweets', showTweets),
    # 更新多用户推文(搜索)
    path('batchUpdateTweetsBySearch', batchUpdateTweetsBySearch),
    # 更新多用户推文(滚动)
    path('batchUpdateTweetsByScroll', batchUpdateTweetsByScroll),
    # 更新多用户推文(定时任务)
    path('batchUpdateTweetsByTask', batchUpdateTweetsByTask),
    # 更新多用户信息
    path('batchUpdateTwitterUserInfo', batchUpdateTwitterUserInfo),
    # 下载视频至本地
    path('downloadVideo', downloadVideo),
    # path('',),
]
