from twitter.models import Tweet, TwitterUser
from .twitterRequestService import *

'''
    推特用户服务
'''


def getUserIdByUsername(username):
    rest_id = TwitterUser.objects.get(username=username).rest_id
    return rest_id


# 分析用户json信息
def analyzeUserInfo(to_db):
    j = open('C:/Users/Lenovo/OneDrive/twitter/1.txt', 'r', encoding="utf-8")  
    o = json.loads(j.read())
    to_db = True
    user = TwitterUser()
    birthday_json = o['data']['user']['result']['legacy_extended_profile'].get('birthdate')
    print(birthday_json)
    year = birthday_json.get('year', '')
    month = birthday_json.get('month', '')
    day = birthday_json.get('day', '')
    user.birthday = str(year) + '-' + \
                    str(month) + '-' + \
                    str(day)  # 生日
    result_json = o['data']['user']['result']
    user.user_id = result_json.get('id')  # 唯一id
    user.rest_id = result_json.get('rest_id')  # rest_id

    legacy_json = result_json['legacy']
    user.name = legacy_json.get('name')  # 名称
    user.username = legacy_json.get('screen_name')  # 唯一用户名
    user.created_at = legacy_json.get('created_at')  # 帐号创建时间
    user.description = legacy_json.get('description')  # 简介
    user.display_url = legacy_json.get('url')  # 展示链接
    user.location = legacy_json.get('location')  # 地点
    user.followers_count = legacy_json.get('followers_count')  # 关注者
    user.friends_count = legacy_json.get('friends_count')  # 正在关注
    if to_db:  # 存入数据库
        user.save()
    else:
        print(user)
