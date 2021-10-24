import requests
import json

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
    r = requests.post(u, params, headers=headers)
    print(r)
    return r


url_token = 'https://api.twitter.com/1.1/guest/activate.json'

# 获取token
def get_token():
    token = json.loads(requests.post(url_token, headers=headers).text)['guest_token']
    print(token)
    headers['x-guest-token'] = token
