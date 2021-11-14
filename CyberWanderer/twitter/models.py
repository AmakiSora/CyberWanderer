from django.db import models


# 任何数据库表结构的修改,必须在对应的模型类修改,修改完成后再次迁移同步(migrate)
# 推文信息
class Tweet(models.Model):
    name = models.CharField('昵称', max_length=1023, default='')
    username = models.CharField('用户名', max_length=255, default='')
    user_id = models.CharField('唯一ID', max_length=255, default='')
    created_at = models.CharField('创建时间', max_length=255, default='')
    created_time = models.DateTimeField("时间", null=True)
    full_text = models.CharField('推文内容', max_length=2047, default='')
    tweet_id = models.CharField('推文ID', max_length=255, null=False, primary_key=True)
    tweet_media_urls = models.CharField('推文媒体地址', max_length=2047, default='')
    tweet_media_local = models.CharField('推文媒体本地目录', max_length=2047, default='')
    tweet_hashtags = models.CharField('推文标签', max_length=255, default='')
    tweet_urls = models.CharField('推文扩展地址', max_length=2047, default='')
    tweet_type = models.CharField('推文类型', max_length=255, default='')
    status = models.CharField('状态', max_length=255, default='')
    quoted_tweet_id = models.CharField('转推id', max_length=255, default='')


# 推特用户信息
class TwitterUser(models.Model):
    name = models.CharField('昵称', max_length=1023, default='')
    username = models.CharField('用户名', max_length=255, default='')
    rest_id = models.CharField('rest_id', max_length=255, default='')
    user_id = models.CharField('用户名', max_length=255, primary_key=True, null=False)
    created_at = models.CharField('帐号创建时间', max_length=255, default='')
    birthday = models.CharField('生日', max_length=255, default='')
    description = models.CharField('简介', max_length=1023, default='')
    friends_count = models.IntegerField('正在关注', default=-1)
    followers_count = models.IntegerField('关注者', default=-1)
    location = models.CharField('地点', max_length=255, default='')
    display_url = models.CharField('展示链接', max_length=255, default='')
    tweet_count = models.IntegerField('推文数', default=0)
