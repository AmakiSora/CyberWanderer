import json
import re

import requests

from twitter.models import Tweet
from twitter.service.twitterRequestService import get_token, headers, get_headers

'''
    推特推文服务
'''


def getTweets(user_id, count, cursor=''):
    u = 'https://twitter.com/i/api/graphql/9R7ABsb6gQzKjl5lctcnxA/UserTweets'
    variables = {
        "userId": user_id,
        "count": count,
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
    if cursor != '':
        variables['cursor'] = cursor

    params = {
        'variables': json.dumps(variables, sort_keys=True, indent=4, separators=(',', ':'))
    }
    tweets_json = requests.post(u, params, headers=get_headers())
    if tweets_json.status_code == 200:
        return json.loads(tweets_json.text)
    return None


# 自动化,最多获取850条数据
def autoGetUserTweets(user_id, count=20, to_db=True, frequency=1):
    tweets_json = getTweets(user_id, count)
    if tweets_json is None:
        return '错误！'
    cursor_bottom = analyzeUserTweets(tweets_json, to_db)
    if frequency > 1:
        for i in range(frequency):
            tweets_json = getTweets(user_id, count, cursor_bottom)
            if cursor_bottom is None:
                return tweets_json
            cursor_bottom = analyzeUserTweets(tweets_json, to_db)

    return tweets_json


# 分析用户推文
def analyzeUserTweets(tweets_json, to_db):
    # j = open('D:\cosmos\OneDrive/twitter/json.txt', 'r', encoding="utf-8")
    # o = json.loads(j.read())
    global cursor_bottom
    instructions = tweets_json['data']['user']['result']['timeline']['timeline']['instructions']
    for i in instructions:
        if i['type'] == 'TimelineAddEntries':  # 推文列
            tweetNum = 0  # 记录推文数,也是终止标签,如果无后续推文,直接终止循环
            tweets = []
            for e in i.get('entries'):
                entryId = e.get('entryId')
                # print('entryId = ', entryId)
                if re.match("^tweet-[0-9]*", entryId):  # 确认为用户推文
                    tweetNum += 1
                    tweet = Tweet()
                    result = e['content']['itemContent']['tweet_results']['result']
                    analyzeTweetsResultJSON(result, tweet, tweets, to_db)
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
            print(tweets)
            print('本次请求一共', tweetNum, "条推文!")
            Tweet.objects.bulk_create(tweets, ignore_conflicts=True)  # 批量存入数据库(忽略重复id)
            if tweetNum == 0:  # 表示后面没有推文了
                return None
        elif i['type'] == 'TimelinePinEntry':  # 置顶推文
            pass
            # print("置顶推文,暂时不处理")
    return cursor_bottom


# 分析推文具体信息
def analyzeTweetsResultJSON(result, tweet, tweets, to_db):
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
        if to_db:
            tweets.append(tweet)
            # tweet.save()  # 保存至数据库
        else:
            print(tweet)
        # 某些推文是转推，但是没有附带quoted_status_result这个转推信息，目前不知道为什么
        quoted_status_result = result.get('quoted_status_result', None)
        if quoted_status_result is not None:
            quoted_result = quoted_status_result.get('result', None)
            if quoted_result is not None:
                quoted_tweet = Tweet()
                analyzeTweetsResultJSON(quoted_result, quoted_tweet, tweets, to_db)

    else:  # 不是转推
        tweet.tweet_type = 'OriginalTweet'  # 推文类型!!!
        if to_db:
            tweets.append(tweet)
            # tweet.save()  # 保存至数据库
        else:
            print(tweet)
