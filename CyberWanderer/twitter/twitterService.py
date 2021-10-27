import re

import requests
import json

from twitter.models import Tweet, TwitterUser

headers = {
    # "Host": "utils.com",
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
    # 'Accept': '*/*',
    # 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'x-guest-token': '',
    # 'x-utils-client-language': 'zh-cn',
    # 'x-utils-active-user': 'yes',
    # 'x-csrf-token': 'feb505674f40e6a83143c6ce4d1f4d04',
    # 'Sec-Fetch-Dest': 'empty',
    # 'Sec-Fetch-Mode': 'cors',
    # 'Sec-Fetch-Site': 'same-origin',
    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    # 'Referer': 'https://twitter.com/',
    # 'Connection': 'keep-alive',
}


def getTweets(url):
    u = 'https://twitter.com/i/api/graphql/eHLYMJzt92nT5THTeJjj8A/UserTweets'
    variables = {
        "userId": "744906956649857024",
        "count": 20,
        "withTweetQuoteCount": True,
        "includePromotedContent": True,
        "withQuickPromoteEligibilityTweetFields": False,
        "withSuperFollowsUserFields": False,
        "withUserResults": True,
        "withBirdwatchPivots": False,
        "withReactionsMetadata": False,
        "withReactionsPerspective": False,
        "withSuperFollowsTweetFields": False,
        "withVoice": True
    }
    params = {
        'variables': json.dumps(variables, sort_keys=True, indent=4, separators=(',', ':'))
    }
    get_token()
    tweetsJSON = requests.post(u, params, headers=headers)
    return tweetsJSON


url_token = 'https://api.twitter.com/1.1/guest/activate.json'


# 获取token
def get_token():
    token = json.loads(requests.post(url_token, headers=headers).text)['guest_token']
    print(token)
    headers['x-guest-token'] = token


# 分析用户推文
def analyzeUserTweets():
    j = open('D:\cosmos\OneDrive/twitter/json.txt', 'r', encoding="utf-8")
    o = json.loads(j.read())
    instructions = o['data']['user']['result']['timeline']['timeline']['instructions']
    for i in instructions:
        if i['type'] == 'TimelineAddEntries':  # 推文列
            for e in i.get('entries'):
                entryId = e.get('entryId')
                print('entryId = ', entryId)
                if re.match("^tweet-[0-9]*", entryId):  # 确认为用户推文
                    tweet = Tweet()
                    result = e['content']['itemContent']['tweet_results']['result']
                    analyzeTweetsResultJSON(result, tweet)
                elif re.match("^homeConversation-[0-9-a-zA-Z]*", entryId):  # 连续推文
                    pass
                    # print("连续推文")
                elif re.match("^promotedTweet-[0-9-a-zA-Z]*", entryId):  # 推广推文(广告)
                    pass
                    # print("推广推文,暂时不处理")
                elif re.match("^whoToFollow-[0-9-a-zA-Z]*", entryId):  # 推荐关注
                    pass
                    # print("推荐关注,暂时不处理")
                elif re.match("^cursor-top-[0-9-a-zA-Z]*", entryId):  # 光标顶部
                    pass
                    # print("光标顶部,暂时不处理")
                elif re.match("^cursor-bottom-[0-9-a-zA-Z]*", entryId):  # 光标底部
                    cursor_bottom = e['content'].get('value')
        elif i['type'] == 'TimelinePinEntry':  # 置顶推文
            pass
            # print("置顶推文,暂时不处理")


# 分析推文具体信息
def analyzeTweetsResultJSON(result, tweet):
    if result['__typename'] == 'TweetUnavailable':
        print('推文不可用')
        return
    tweet.name = result['core']['user_results']['result']['legacy']['name']  # 名称
    tweet.username = result['core']['user_results']['result']['legacy']['screen_name']  # 唯一用户名
    tweet.user_id = result['core']['user_results']['result']['id']  # 唯一id
    tweet.tweet_id = result['legacy']['id_str']  # 推文id
    tweet.full_text = result['legacy']['full_text']  # 推文内容
    tweet.created_at = result['legacy']['created_at']  # 创建时间

    hashtags_list = result['legacy']['entities'].get('hashtags')
    if hashtags_list is not None:  # 有标签
        tag = ''
        for h in hashtags_list:
            tag = tag + '#' + h.get('text')
        tweet.tweet_hashtags = tag  # 标签

    media_list = result['legacy']['entities'].get('media')
    if media_list is not None:
        media_url = ''
        for m in media_list:
            media_url = media_url + '|' + m.get('media_url_https')
        tweet.tweet_media_urls = media_url  # 推文图片地址

    urls_list = result['legacy']['entities'].get('urls')
    if urls_list is not None:
        urls = ''
        for u in urls_list:
            urls = urls + '|' + u.get('expanded_url')
        tweet.tweet_urls = urls  # 推文附加地址
    if result['legacy'].get('is_quote_status'):  # true为转推 false不是
        tweet.tweet_type = 'Retweeted'  # 推文类型!!!
        tweet.quoted_tweet_id = result['legacy'].get('quoted_status_id_str')  # 转推id
        tweet.save()  # 保存至数据库
        # 某些推文是转推，但是没有附带quoted_status_result这个转推信息，目前不知道为什么
        quoted_result = result.get('quoted_status_result').get('result')
        if quoted_result is not None:
            quoted_tweet = Tweet()
            analyzeTweetsResultJSON(quoted_result, quoted_tweet)
    else:  # 不是转推
        tweet.tweet_type = 'OriginalTweet'  # 推文类型!!!
        tweet.save()  # 保存至数据库


# 分析用户json信息
def analyzeUserInfo(to_db):
    j = open('', 'r', encoding="utf-8")  # todo 待验证
    o = json.loads(j.read())
    to_db = True
    user = TwitterUser()
    birthday_json = o['data']['user']['result']['legacy_extended_profile']['birthdate']
    user.birthday = birthday_json.get('year') + '-' + \
                    birthday_json.get('month') + '-' + \
                    birthday_json.get('day')  # 生日
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

# analyzeUserTweets()
# analyzeUserInfo()
