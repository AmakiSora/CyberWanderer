from django.contrib import admin

# 注册模型类到管理页面
from bilibili.models import BiliBiliUser, BiliBiliDynamic


class BiliBiliUserManager(admin.ModelAdmin):
    list_display = ['uid', 'name', 'dynamic_count', 'sign']
    list_display_links = ['uid']
    # list_filter = ['created_time']


class BiliBiliDynamicManager(admin.ModelAdmin):
    # 列表页展示字段
    list_display = ['dynamic_id', 'name', 'created_time', 'full_text', 'dynamic_type', 'status']
    # 进入编辑页面点击的字段
    list_display_links = ['dynamic_id']
    # 增加过滤器
    list_filter = ['created_time', 'dynamic_type', 'status']
    # 添加搜索框(只搜索以下字段)
    search_fields = ['name', 'full_text']
    # 添加可在列表页编辑的字段
    list_editable = ['status']


admin.site.register(BiliBiliUser, BiliBiliUserManager)
admin.site.register(BiliBiliDynamic, BiliBiliDynamicManager)
