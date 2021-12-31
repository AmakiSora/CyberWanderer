from django.db import models


# 用户信息
class BiliBiliUser(models.Model):
    uid = models.CharField('用户唯一id', max_length=255, primary_key=True, null=False)
    name = models.CharField('昵称', max_length=255, default='')
    avatar_url = models.CharField('头像url', max_length=1023, default='')
    sign = models.CharField('简介', max_length=1023, default='')
    birthday = models.CharField('生日', max_length=255, default='')
    level = models.IntegerField('等级', default=-1)
    friends_count = models.IntegerField('正在关注', default=-1)
    followers_count = models.IntegerField('关注者', default=-1)
    dynamic_count = models.IntegerField('动态数', default=0)


# 动态信息
class BiliBiliDynamic(models.Model):
    dynamic_id = models.CharField('动态id', max_length=255, primary_key=True)
    name = models.CharField('昵称', max_length=255, default='')
    uid = models.CharField('用户唯一id', max_length=255, default='')
    created_time = models.DateTimeField("动态时间", null=True)
    full_text = models.CharField('动态内容', max_length=2047, default='')
    dynamic_media_urls = models.CharField('动态媒体地址', max_length=2047, default='')
    bvid = models.CharField('视频bv号', max_length=255, default='')
    dynamic_urls = models.CharField('动态扩展地址', max_length=2047, default='')
    dynamic_type = models.CharField('动态类型', max_length=255, default='')
    status = models.CharField('状态', max_length=255, default='')
    quoted_dynamic_id = models.CharField('转载动态id', max_length=255, default='')


class BiliBiliVideo(models.Model):
    bvid = models.CharField('视频bv号', max_length=255, primary_key=True)
    title = models.CharField('标题', max_length=255)
    description = models.CharField('视频简介', max_length=2047, default='')
    created_time = models.DateTimeField("投稿时间", null=True)
    uid = models.CharField('up主uid', max_length=255, default='')
    name = models.CharField('昵称', max_length=255, default='')
    pic = models.CharField('视频封面', max_length=255, default='')
