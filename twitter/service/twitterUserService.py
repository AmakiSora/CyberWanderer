import datetime
import logging

from twitter.models import Tweet, TwitterUser
from .twitterRequestService import *
import logging

from .userTweetsService import updateTweetCount

'''
    推特用户服务
'''
logger = logging.getLogger(__name__)


# 根据username获取rest_id
def getRestIdByUsername(username):
    try:
        rest_id = TwitterUser.objects.get(username=username).rest_id
    except:
        return None
    return rest_id


def getUserInfo(username):
    u = 'https://twitter.com/i/api/graphql/cYsDlVss-qimNYmNlb6inw/UserByScreenName'
    variables = {
        "screen_name": username,
        # "withSafetyModeUserFields": True,
        "withSuperFollowsUserFields": True
    }
    params = {
        'variables': json.dumps(variables, sort_keys=True, indent=4, separators=(',', ':'))
    }
    info_json = requests.get(u, params, headers=get_headers(), proxies=settings.PROXIES)
    if info_json.status_code == 200:
        return json.loads(info_json.text)
    return None


# 自动化
def autoGetUserInfo(username, to_db):
    info_json = getUserInfo(username)
    re = analyzeUserInfo(info_json, to_db)
    return re


# 分析用户json信息
def analyzeUserInfo(info_json, to_db):
    # j = open('C:/Users/Lenovo/OneDrive/twitter/1.txt', 'r', encoding="utf-8")
    # o = json.loads(j.read())
    user = TwitterUser()
    birthday_json = info_json['data']['user']['result']['legacy_extended_profile'].get('birthdate')
    if birthday_json is not None:
        year = birthday_json.get('year', '')
        month = birthday_json.get('month', '')
        day = birthday_json.get('day', '')
        user.birthday = str(year) + '-' + \
                        str(month) + '-' + \
                        str(day)  # 生日

    result_json = info_json['data']['user']['result']
    user.user_id = result_json.get('id')  # 唯一id
    user.rest_id = result_json.get('rest_id')  # rest_id

    legacy_json = result_json['legacy']
    user.name = legacy_json.get('name')  # 名称
    user.username = legacy_json.get('screen_name')  # 唯一用户名
    user.created_at = legacy_json.get('created_at')  # 帐号创建时间
    user.created_time = datetime.datetime.strptime(user.created_at, '%a %b %d %H:%M:%S +0000 %Y')
    user.description = legacy_json.get('description')  # 简介
    user.display_url = legacy_json.get('url', '')  # 展示链接
    user.location = legacy_json.get('location')  # 地点
    user.followers_count = legacy_json.get('followers_count')  # 关注者
    user.friends_count = legacy_json.get('friends_count')  # 正在关注
    if to_db:  # 存入数据库
        user.save()
        logger.info(str(str(user.username) + "加入数据库"))
        updateTweetCount(user.username)
    else:
        logger.info(user.__str__())
    return '用户名: @' + user.username + ' ,昵称: ' + user.name


def updateTwitterUserInfo(**filter_obj):
    twitter_users = TwitterUser.objects.filter(**filter_obj)
    if twitter_users.count() == 0:
        return '未找到筛选的用户!!!'
    for info in twitter_users:
        re = autoGetUserInfo(info.username, True)
        logger.info(re)
    return '共更新了 ' + str(twitter_users.count()) + ' 个推特用户信息'
