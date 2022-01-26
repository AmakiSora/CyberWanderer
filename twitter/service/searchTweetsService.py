'''
    搜索推特推文服务
    可搜到历史信息,理论上能收集全
'''
import asyncio
import datetime
import json
import aiohttp
import requests
from asgiref.sync import sync_to_async

from CyberWanderer import settings
from CyberWanderer.utils import threadUtil
from twitter.models import Tweet
from twitter.service.twitterRequestService import get_headers, get_token
import logging

logger = logging.getLogger(__name__)


# 获取基本参数
def get_params():
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
    return params


# 获取用户搜索推文()
def get_user_search_tweets(username, since, until, cursor=''):
    url = 'https://twitter.com/i/api/2/search/adaptive.json'
    params = get_params()
    if cursor != '':
        params['cursor'] = cursor
    q = '(from:' + username + ')until:' + until + ' since:' + since
    logger.info(q)
    params['q'] = q
    try:
        tweets_json = requests.get(url, params, headers=get_headers(), proxies=settings.PROXIES)
    except:
        logger.error("太频繁啦，慢点")
        return None
    if tweets_json.status_code == 200:
        return json.loads(tweets_json.text)
    else:
        logger.error('出错啦,报错信息:' + str(tweets_json.text))
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
            logger.info(str("执行分析区间: " + str(since) + ' - ' + str(until) + ' 剩余天数：' + str(dc - intervalDays)))
            # print("执行分析区间:", since, '-', until, '剩余天数：', dc - intervalDays)
            since = until
            until = since + datetime.timedelta(days=intervalDays)
            if (until_all - until).days < 0:
                until = until_all
            dc = (until_all - since).days
        else:
            loopAnalysis(username, since.strftime('%Y-%m-%d'), until.strftime('%Y-%m-%d'))
            logger.info(str("执行分析区间: " + str(since) + ' - ' + str(until) + ' 剩余天数：' + str(dc - intervalDays)))
            # print("执行分析区间:", since, '-', until, '剩余天数：', dc - intervalDays)
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
    if tweets_json is None:
        logger.error("tweets_json获取出错,tweets_json->")
        return ''
    global_Objects = tweets_json.get('globalObjects')
    g_tweets = global_Objects.get('tweets')
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
        if to_db:
            sync_to_async(tweet.save(), thread_sensitive=True)  # 保存至数据库
        else:
            logger.info(tweet.username + ':' + tweet.full_text)
        count += 1
    logger.info('一共 ' + str(count) + ' 条推文')
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


# -------------------------------------------------------------------------------------------------------

# 自动获取搜索推文(异步)
def auto_get_user_search_tweets_async(username, since_all_str, until_all_str, intervalDays=30):
    # 协程获取推文
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # 使用代理必须要的,可能是windows的原因
    re = asyncio.run(coroutine(username, since_all_str, until_all_str, intervalDays))
    # 多线程处理推文
    code, statusInfo = threadUtil.multithreading_list(re, multithreadingHandle, params=None)
    # 如果还有未获取完后续的推文,继续循环获取
    while len(statusInfo) > 2:
        # 更换参数
        get_token()
        # 协程获取推文
        re = asyncio.run(coroutine_next(username, statusInfo, intervalDays))
        # 多线程处理推文
        code, statusInfo = threadUtil.multithreading_list(re, multithreadingHandle, params=None)


# 协程处理(第一次请求)
async def coroutine(username, since_all_str, until_all_str, intervalDays=30):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), trust_env=True) as session:
        tasks = [
            asyncio.create_task(get_user_search_tweets_coroutine(username, start, intervalDays, session, '')) for start
            in get_timedelta_list(since_all_str, until_all_str, intervalDays)
        ]
        done, pending = await asyncio.wait(tasks)
        return done


# 获取时间间隔数组(协程)
def get_timedelta_list(since_all_str, until_all_str, intervalDays):
    result = []
    start = datetime.datetime.strptime(since_all_str, '%Y-%m-%d')
    end = datetime.datetime.strptime(until_all_str, '%Y-%m-%d')
    while start <= end:
        result.append(start)
        start = start + datetime.timedelta(days=intervalDays)
    return result


# 获取用户搜索推文(协程)
async def get_user_search_tweets_coroutine(username, start, intervalDays, session, cursor=''):
    url = 'https://twitter.com/i/api/2/search/adaptive.json'
    params = get_params()
    if cursor != '':
        params['cursor'] = cursor
    since = str(start.strftime('%Y-%m-%d'))
    until = str((start + datetime.timedelta(days=intervalDays)).strftime('%Y-%m-%d'))
    q = '(from:' + username + ')until:' + until + ' since:' + since
    logger.info(q)
    params['q'] = q
    async with session.get(url,
                           data=params,
                           headers=get_headers(),
                           proxy=settings.PROXIES.get('http'),
                           verify_ssl=False) as response:
        if response.status == 200:
            re = await response.text()
            tweets_json = json.loads(re)
            # 将查询条件也返回(后面用于获取后续推文)
            return tweets_json, start
    return None


# 多线程处理json
def multithreadingHandle(task):
    t = task.result()
    # t[0]为json信息,t[1]为开始日期
    cursor = analyze_search_tweets(t[0], True)
    if cursor != '':
        return cursor, t[1]
    else:
        return '无了', None


# 协程处理(后续请求)
async def coroutine_next(username, statusInfo, intervalDays=30):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), trust_env=True) as session:
        tasks = []
        for i in statusInfo:
            if i != 'count' and i != '无了':
                tasks.append(asyncio.create_task(
                    get_user_search_tweets_coroutine(username, statusInfo[i], intervalDays, session, i)))
        done, pending = await asyncio.wait(tasks)
        return done
