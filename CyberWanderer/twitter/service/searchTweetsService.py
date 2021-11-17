'''
    搜索推特推文服务
    可搜到历史信息,理论上能收集全
'''
import datetime
import json

import requests

from CyberWanderer import settings
from twitter.models import Tweet
from twitter.service.twitterRequestService import get_headers, get_token


# 获取用户搜索推文()
def get_user_search_tweets(username, since, until, cursor=''):
    url = 'https://twitter.com/i/api/2/search/adaptive.json'
    params = {
        'include_profile_interstitial_type': 1,  # 包括配置文件插页式类型
        'include_blocking': 1,  # 包括阻塞
        'include_blocked_by': 1,  # 包括被阻止
        'include_followed_by': 1,  # 包括跟随
        'include_want_retweets': 1,  # 包括转发
        'include_mute_edge': 1,  #
        'include_can_dm': 1,  #
        'include_can_media_tag': 1,  # 能被媒体标记
        'skip_status': 1,  # 跳过状态
        'cards_platform': 'Web-12',  # 平台
        'include_cards': 1,  # 卡片
        'include_ext_alt_text': True,  # 包括额外文本
        'include_quote_count': True,  # 引用计数
        'include_reply_count': 1,  # 回复计数
        'tweet_mode': 'extended',  # 推特模式:扩展
        'include_entities': True,  # 实体
        'include_user_entities': True,  # 用户实体
        'include_ext_media_color': True,  # 外部媒体颜色
        'include_ext_media_availability': True,  # 外部媒体可用性
        'send_error_codes': True,  # 发送错误代码
        'simple_quoted_tweet': True,  # 简单引用的推文
        'q': '',  # 查询内容
        # 'count': 200,  # 总计查询条数
        'query_source': 'typed_query',  # 查询源:类型查询
        'pc': 1,  # PC
        'spelling_corrections': 1,  # 拼写更正
        'include_ext_has_nft_avatar': False,  # 包括头像
        'ext': 'mediaStats%2ChighlightedLabel%2CvoiceInfo%2CsuperFollowMetadata'  # 额外
    }
    if cursor != '':
        params['cursor'] = cursor
    q = '(from:' + username + ')until:' + until + ' since:' + since
    print(q)
    params['q'] = q
    try:
        tweets_json = requests.get(url, params, headers=get_headers(), proxies=settings.PROXIES)
    except:
        print("太频繁啦，慢点")
        return None
    if tweets_json.status_code == 200:
        return json.loads(tweets_json.text)
    else:
        print('出错啦,报错信息:', tweets_json.text)
    return None


# 自动获取搜索内容推文
def auto_get_user_search_tweets(username, since_all_str, until_all_str, to_db=True, intervalDays=30):
    since_all = datetime.datetime.strptime(since_all_str, '%Y-%m-%d')
    until_all = datetime.datetime.strptime(until_all_str, '%Y-%m-%d')
    dc = (until_all - since_all).days
    since = since_all
    until = since + datetime.timedelta(days=intervalDays)
    refreshToken = 0
    while dc > 0:
        if dc > intervalDays:
            loopAnalysis(username, since.strftime('%Y-%m-%d'), until.strftime('%Y-%m-%d'))
            print("执行分析区间:", since, '-', until, '剩余天数：', dc - intervalDays)
            since = until
            until = since + datetime.timedelta(days=intervalDays)
            if (until_all - until).days < 0:
                until = until_all
            dc = (until_all - since).days
        else:
            loopAnalysis(username, since.strftime('%Y-%m-%d'), until.strftime('%Y-%m-%d'))
            print("执行分析区间:", since, '-', until, '剩余天数：', dc - intervalDays)
            dc = dc - intervalDays
        refreshToken += 1
        if refreshToken > 10:
            refreshToken = 0
            get_token()


# 循环解析
def loopAnalysis(username, since, until):
    cursor = analyze_search_tweets(get_user_search_tweets(username, since, until))
    while cursor != '':
        tweets_json = get_user_search_tweets(username, since, until, cursor=cursor)
        cursor = analyze_search_tweets(tweets_json)


# 分析搜索推文
def analyze_search_tweets(tweets_json, to_db=True):
    g_tweets = tweets_json['globalObjects']['tweets']
    g_users = tweets_json['globalObjects']['users']
    count = 0
    for i in g_tweets:
        tweet = Tweet()
        tweet.tweet_id = i
        tweet.created_at = g_tweets[i].get('created_at')
        tweet.created_time = datetime.datetime.strptime(tweet.created_at, '%a %b %d %H:%M:%S +0000 %Y')
        tweet.full_text = g_tweets[i].get('full_text')
        tweet.user_id = g_tweets[i].get('user_id_str')
        tweet.username = g_users[tweet.user_id].get('screen_name')
        tweet.name = g_users[tweet.user_id].get('name')
        if g_tweets[i].get('is_quote_status'):
            tweet.tweet_type = 'Retweeted'  # 推文类型!!!
            tweet.quoted_tweet_id = g_tweets[i].get('quoted_status_id_str', '')
        else:
            tweet.tweet_type = 'OriginalTweet'  # 推文类型!!!

        entities = g_tweets[i]['entities']
        hashtags_list = entities.get('hashtags')
        if hashtags_list is not None:  # 有标签
            tag = ''
            for h in hashtags_list:
                tag = tag + '#' + h.get('text')
            tweet.tweet_hashtags = tag  # 标签

        media_list = entities.get('media')
        if media_list is not None:
            media_url = ''
            for m in media_list:
                media_url = media_url + '|' + m.get('media_url_https')
            tweet.tweet_media_urls = media_url  # 推文图片地址

        urls_list = entities.get('urls')
        if urls_list is not None:
            urls = ''
            for u in urls_list:
                urls = urls + '|' + u.get('expanded_url')
            tweet.tweet_urls = urls  # 推文附加地址
        tweet.save()  # 保存至数据库
        count += 1
    print('一共', count, '条推文')
    cursor_bottom = ''
    if count == 0:
        return cursor_bottom
    instructions = tweets_json['timeline']['instructions']
    for i in instructions:
        if i.get('addEntries') is not None:
            for j in i['addEntries'].get('entries'):
                if j['entryId'] == 'sq-cursor-bottom':
                    cursor_bottom = j['content']['operation']['cursor'].get('value', '')
                    return cursor_bottom
        elif i.get('replaceEntry') is not None:
            if i['replaceEntry'].get('entryIdToReplace', '') == 'sq-cursor-bottom':
                cursor_bottom = i['replaceEntry']['entry']['content']['operation']['cursor'].get('value', '')
                return cursor_bottom

    return cursor_bottom
