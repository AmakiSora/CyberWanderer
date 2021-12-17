from django.contrib import admin
from .models import Tweet
from .models import TwitterUser


# 注册模型类到管理页面
class TweetManager(admin.ModelAdmin):
    # 列表页展示字段
    list_display = ['tweet_id', 'username', 'created_time', 'full_text', 'tweet_type', 'status']
    # 进入编辑页面点击的字段
    list_display_links = ['tweet_id']
    # 增加过滤器
    list_filter = ['created_time', 'tweet_type', 'status']
    # 添加搜索框(只搜索以下字段)
    search_fields = ['username', 'full_text']
    # 添加可在列表页编辑的字段
    list_editable = ['status']


class TwitterUserManager(admin.ModelAdmin):
    list_display = ['username', 'name', 'tweet_count', 'description', 'created_at']
    list_display_links = ['username']
    # list_filter = ['created_time']


admin.site.register(Tweet, TweetManager)
admin.site.register(TwitterUser, TwitterUserManager)
