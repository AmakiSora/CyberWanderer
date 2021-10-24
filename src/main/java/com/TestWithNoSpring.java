package com;

import com.utils.ConnectionUtils;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URL;
import java.net.URLConnection;
import java.net.http.HttpClient;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 测试用
 */
public class TestWithNoSpring {
    public static void main(String[] args) throws IOException {
//        ConnectionUtils connectionUtils = new ConnectionUtils();
//        HashMap<String, String> map = new HashMap<>();
//        map.put("Host","twitter.com");
//        map.put("x-guest-token","1450841120372523011");
//        map.put("Authorization","Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA");
//        try {
//            String json = connectionUtils.getJsonFromApiByHeader("https://twitter.com/i/api/graphql/eHLYMJzt92nT5THTeJjj8A/UserTweets?variables=%7B%22userId%22%3A%22744906956649857024%22%2C%22count%22%3A20%2C%22withTweetQuoteCount%22%3Atrue%2C%22includePromotedContent%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Afalse%2C%22withUserResults%22%3Atrue%2C%22withBirdwatchPivots%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Afalse%2C%22withVoice%22%3Atrue%7D", map);
//            System.out.println(json);
//        } catch (Exception e) {
//            e.printStackTrace();
//        }
        System.out.println(te());
    }
    public static String te(){
        try {
            URL url = URI.create("https://twitter.com/i/api/graphql/eHLYMJzt92nT5THTeJjj8A/UserTweets?variables=%7B%22userId%22%3A%22744906956649857024%22%2C%22count%22%3A20%2C%22withTweetQuoteCount%22%3Atrue%2C%22includePromotedContent%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Afalse%2C%22withUserResults%22%3Atrue%2C%22withBirdwatchPivots%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Afalse%2C%22withVoice%22%3Atrue%7D").toURL();
//            URL url = URI.create("https://baidu.com").toURL();
            HttpURLConnection httpURLConnection;
            httpURLConnection = (HttpURLConnection) url.openConnection();
            httpURLConnection.setRequestMethod("GET");
            System.setProperty("sun.net.http.allowRestrictedHeaders", "true");
            httpURLConnection.setRequestProperty("Host","twitter.com");
            httpURLConnection.setRequestProperty("x-guest-token","1450841120372523011");
            httpURLConnection.setRequestProperty("Authorization","Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA");
            System.out.println(httpURLConnection.getHeaderField("Host"));
            System.out.println(httpURLConnection.getHeaderFields());
            System.out.println(httpURLConnection.getRequestProperties());
            System.out.println(httpURLConnection.getResponseCode());
            return "httpURLConnection.getResponseCode()";
        } catch (IOException e) {
            e.printStackTrace();
        }
        return "";
    }
}
