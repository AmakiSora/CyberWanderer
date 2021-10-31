'''
    搜索推特推文服务
    可搜到历史信息,理论上能收集全
'''
import json

import requests

from twitter.service.twitterRequestService import get_headers


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
    tweets_json = requests.get(url, params, headers=get_headers())
    if tweets_json.status_code == 200:
        return json.loads(tweets_json.text)
    else:
        print('出错啦,报错信息:', tweets_json.text)
    return None


# 自动获取搜索内容推文
def auto_get_user_search_tweets(username, since_all_str, until_all_str, to_db=True):
    # since_all = datetime.datetime.strptime(since_all_str, '%Y-%m-%d')
    # until_all = datetime.datetime.strptime(until_all_str, '%Y-%m-%d')
    # dc = (until_all - since_all).days
    # print(dc)
    # while dc > 0:
    #     if (until_all - since_all).days > 30:
    #         since = d2
    #         print(since)
    #         d2 = d2 - datetime.timedelta(days=30)
    #         until = d2
    #         print(until)
    #         tweets_json = get_user_search_tweets(username, since, until, to_db)
    #     else:
    #         tweets_json = get_user_search_tweets(username, since, until, to_db)
    a = get_user_search_tweets(username, since_all_str, until_all_str)
    cursor = analyze_search_tweets(a)
    while cursor != '':
        tweets_json = get_user_search_tweets(username, since_all_str, until_all_str, cursor=cursor)
        cursor = analyze_search_tweets(tweets_json)


# 分析搜索推文
def analyze_search_tweets(tweets_json, to_db=True):
    g_tweets = tweets_json['globalObjects']['tweets']
    count = 0
    for i in g_tweets:
        print(i)
        print(g_tweets[i].get('created_at'))
        print(g_tweets[i].get('full_text'))
        print(g_tweets[i].get('user_id_str'))
        print(g_tweets[i].get('is_quote_status'))
        if g_tweets[i].get('is_quote_status') == True:
            print(g_tweets[i].get('quoted_status_id_str'))

        entities = g_tweets[i]['entities']
        user_mentions = entities.get('user_mentions')
        print(user_mentions)
        if user_mentions is not None and user_mentions != []:
            for j in user_mentions:
                print(j.get('screen_name'))
                print(j.get('name'))

        print("----------------------------------------------")

        count += 1
    print('一共', count, '条推文')
    cursor_bottom = ''
    if count == 0:
        return cursor_bottom
    instructions = tweets_json['timeline']['instructions']
    print(instructions)
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


# auto_get_user_search_tweets('Liyu0109', '2016-7-1', '2017-1-1')
