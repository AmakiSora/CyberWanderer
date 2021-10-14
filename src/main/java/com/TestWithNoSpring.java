package com;

import com.twitter.service.TwitterTweetService;
import com.utils.ConnectionUtils;

import java.io.*;
import java.util.HashMap;

/**
 * 测试用,不用启动springboot
 */
public class TestWithNoSpring {
    public static void main(String[] args) throws IOException {
        ConnectionUtils connectionUtils = new ConnectionUtils();
        HashMap<String, String> map = new HashMap<>();
        map.put("x-guest-token","1448187382679801856");
        map.put("Authorization","Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA");
        try {
            String json = connectionUtils.getJsonFromApiByHeader("https://twitter.com/i/api/graphql/p68c7OTFDZVMpkCA1-x3rg/UserTweets?variables=%7B%22userId%22%3A%222859339990%22%2C%22count%22%3A20%2C%22withTweetQuoteCount%22%3Atrue%2C%22includePromotedContent%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Afalse%2C%22withUserResults%22%3Atrue%2C%22withBirdwatchPivots%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Afalse%2C%22withVoice%22%3Atrue%7D", map);
            new TwitterTweetService().analyzeUserTweetsJSON(json);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
//    curl 'https://twitter.com/i/api/graphql/p68c7OTFDZVMpkCA1-x3rg/UserTweets?variables=%7B%22userId%22%3A%222859339990%22%2C%22count%22%3A20%2C%22withTweetQuoteCount%22%3Atrue%2C%22includePromotedContent%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Afalse%2C%22withUserResults%22%3Atrue%2C%22withBirdwatchPivots%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Afalse%2C%22withVoice%22%3Atrue%7D' \
//            -X 'GET' \
//            -H 'Content-Type: application/json' \
//            -H 'Accept: */*' \
//            -H 'Authorization: Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA' \
//            -H 'Accept-Language: zh-cn' \
//            -H 'Accept-Encoding: gzip, deflate, br' \
//            -H 'Host: twitter.com' \
//            -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15' \
//            -H 'Referer: https://twitter.com/mydreams_Ayumu' \
//            -H 'Connection: keep-alive' \
//            -H 'Cookie: gt=1448187382679801856; ct0=c4cf23198ab4fa4136c8f13aa9b34146; guest_id=v1%3A161949787518603486; personalization_id="v1_u1zLFTXXA5//uLe/Ap28xg=="' \
//            -H 'x-guest-token: 1448187382679801856' \
//            -H 'x-twitter-client-language: zh-cn' \
//            -H 'x-csrf-token: c4cf23198ab4fa4136c8f13aa9b34146' \
//            -H 'x-twitter-active-user: yes'

//variables=%7B%22userId%22%3A%222859339990%22%2C%22count%22%3A20%2C%22cursor%22%3A%22HBaKwKPxveuzlSgAAA%3D%3D%22%2C%22withTweetQuoteCount%22%3Atrue%2C%22includePromotedContent%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Afalse%2C%22withUserResults%22%3Atrue%2C%22withBirdwatchPivots%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Afalse%2C%22withVoice%22%3Atrue%7D
}
