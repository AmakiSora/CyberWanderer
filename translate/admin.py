from django.contrib import admin
from translate.models import Translation


# 注册模型类到管理页面
class TranslateManager(admin.ModelAdmin):
    # 列表页展示字段
    list_display = [
        'from_id',
        'target_language',
        'original_text',
        'baidu_translation',
        'youdao_translation',
        'tencent_translation',
        'fanyigou_translation',
        'deepL_translation',
        'google_translation',
    ]
    # 进入编辑页面点击的字段
    list_display_links = ['original_text']
    # 增加过滤器
    # list_filter = ['from_id']
    # 添加搜索框(只搜索以下字段)
    search_fields = ['from_id', 'original_text']
    # 添加可在列表页编辑的字段
    # list_editable = ['']


admin.site.register(Translation, TranslateManager)
