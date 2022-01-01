"""
    推文展示服务
"""
import json

from django.core.serializers.json import DjangoJSONEncoder

from twitter.models import Tweet


def show_user_tweets(**params):
    tweets = Tweet.objects.filter(**params).order_by('-created_time')
    return json.dumps(list(tweets.values()), ensure_ascii=False, cls=DjangoJSONEncoder)
