package com.twitter.service;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.twitter.pojo.Tweet;
import com.twitter.pojo.TwitterUser;
import com.twitter.twitterDataDao.TwitterDataDao;
import com.utils.ConnectionUtils;
import com.utils.ImgDownloadUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.annotation.processing.SupportedOptions;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

@Service
public class TwitterTweetService {
    @Autowired
    private TwitterDataDao twitterDataDao;
    @Autowired
    private TwitterUserService twitterUserService;

    public String analyzeUserTweetsJSON(String data) {
        System.out.println("开始解析推文JSON");
//        JSONObject json = JSONObject.parseObject(a.toString());
        String cursor_bottom = "";
        JSONObject json = (JSONObject) JSON.parse(data);
        JSONObject timelineJson = json.getJSONObject("data")
                .getJSONObject("user")
                .getJSONObject("result")
                .getJSONObject("timeline")
                .getJSONObject("timeline");
        List<JSONObject> instructionsList = (List<JSONObject>) timelineJson.get("instructions");
        List<Tweet> tweets = new ArrayList<>();//提取完成后的推文数组
        for (JSONObject d : instructionsList) {
            //所有的推文,instructionsList的下一组是置顶推文(TimelinePinEntry),现在暂时不理
            if ("TimelineAddEntries".equals(d.get("type"))) {
                List<JSONObject> entriesList = (List<JSONObject>) d.get("entries");
                for (JSONObject dd : entriesList) {
                    String entryId = dd.getString("entryId");
                    if (entryId.matches("^tweet-[0-9]*")) { //确认为用户推文
                        Tweet tweet = new Tweet();
                        JSONObject result = dd.getJSONObject("content")
                                .getJSONObject("itemContent")
                                .getJSONObject("tweet_results")
                                .getJSONObject("result");
                        analyzeTweetsResultJSON(result, tweet, tweets);

                    } else if (entryId.matches("^homeConversation-[0-9-a-zA-Z]*")) { //连续推文
//                        System.out.println("连续推文");
                    } else if (entryId.matches("^promotedTweet-[0-9-a-zA-Z]*")) { //推广推文(广告)
//                        System.out.println("推广推文,暂时不处理");
                    } else if (entryId.matches("^whoToFollow-[0-9-a-zA-Z]*")) { //推荐关注
//                        System.out.println("推荐关注,暂时不处理");
                    } else if (entryId.matches("^cursor-top-[0-9-a-zA-Z]*")) { //光标顶部
//                        System.out.println("光标顶部,暂时不处理");
                    } else if (entryId.matches("^cursor-bottom-[0-9-a-zA-Z]*")) { //光标底部
                        JSONObject content = (JSONObject) dd.get("content");
//                        if (content.getBoolean("stopOnEmptyResponse")){//停止
//                            System.out.println("stopOnEmptyResponse");
//                            cursor_bottom = null;
//                        }else {
                            cursor_bottom = content.getString("value");
//                        }
                    }
                }
            } else if ("TimelinePinEntry".equals(d.get("type"))) {//置顶推文
//                System.out.println("TimelinePinEntry,暂时不处理");
            }
        }
        System.out.println("一共" + tweets.size() + "条推文");
        twitterDataDao.insertTweets(tweets);
        return cursor_bottom;
    }

    private void analyzeTweetsResultJSON(JSONObject result, Tweet tweet, List<Tweet> tweets) {//用于分析推文里的Result
        if ("TweetUnavailable".equals(result.getString("__typename"))){//推文不可用
            System.out.println("推文不可用");
            return;
        }
        String name = result.getJSONObject("core")
                .getJSONObject("user_results")
                .getJSONObject("result")
                .getJSONObject("legacy")
                .getString("name");
        tweet.setName(name);//名称

        String username = result.getJSONObject("core")
                .getJSONObject("user_results")
                .getJSONObject("result")
                .getJSONObject("legacy")
                .getString("screen_name");
        tweet.setUsername(username);//唯一用户名

        String id = result.getJSONObject("core")
                .getJSONObject("user_results")
                .getJSONObject("result")
                .getString("id");
        tweet.setUser_id(id);//唯一id

        JSONObject legacy = result.getJSONObject("legacy");
        tweet.setTweet_id(legacy.getString("id_str"));//推文id
        tweet.setFull_text(legacy.getString("full_text"));//推文内容
        tweet.setCreated_at(legacy.getString("created_at"));//创建时间

        JSONObject entities = legacy.getJSONObject("entities");
        List<JSONObject> hashtags_List = (List<JSONObject>) entities.get("hashtags");
        if (hashtags_List != null && !hashtags_List.isEmpty()) { //有标签
            StringBuilder tag = new StringBuilder();
            for (JSONObject h : hashtags_List) {
                tag.append("#").append(h.getString("text"));
            }
            tweet.setTweet_hashtags(tag.toString());//推文标签
        }

        List<JSONObject> media_List = (List<JSONObject>) entities.get("media");
        if (media_List != null && !media_List.isEmpty()) {
            StringBuilder media_urls = new StringBuilder();
            for (JSONObject m : media_List) {
                media_urls.append("|").append(m.getString("media_url_https"));
            }
            tweet.setTweet_media_urls(media_urls.toString());//推文图片地址
        }

        List<JSONObject> urls_list = (List<JSONObject>) entities.get("urls");
        if (urls_list != null && !urls_list.isEmpty()) {
            StringBuilder urls = new StringBuilder();
            for (JSONObject m : urls_list) {
                urls.append("|").append(m.getString("expanded_url"));
            }
            tweet.setTweet_urls(urls.toString());//推文附加地址
        }
        if (legacy.getBoolean("is_quote_status")) { //true为转推 false不是
            tweet.setTweet_type("Retweeted");//推文类型!!!
            tweet.setQuoted_tweet_id(legacy.getString("quoted_status_id_str"));//转推id
            tweets.add(tweet);
            try { //todo 某些推文是转推，但是没有附带quoted_status_result这个转推信息，目前不知道为什么
                JSONObject quotedResult = result.getJSONObject("quoted_status_result").getJSONObject("result");
                analyzeTweetsResultJSON(quotedResult, new Tweet(), tweets);//递归分析转推的推文
            } catch (NullPointerException e) {
                System.out.println("推文id：" + tweet.getTweet_id() + "是转推，但quoted_status_result为空");
            }
        } else {
            tweet.setTweet_type("OriginalTweet");
            tweets.add(tweet);
        }
    }

    public String downloadImg(String username) {
        if (!username.isBlank()) {
            List<String> list = twitterDataDao.queryImgUrlsByUsername(username);
            List<String> finalList = new ArrayList<>();
            for (String s : list) {
                if (s != null && !s.isBlank()) {
                    String[] split = s.split("\\|");
                    for (String sp : split) {
                        if (!sp.isBlank())
                            finalList.add(sp);
                    }
                }
            }
            new ImgDownloadUtils().processSync(finalList, username);
        } else {//无输入username的情况
//            twitterDataDao
        }
        return "成功";
    }

    public String autoGetUserTweets(String token,String username, Integer onceGetNum, Integer frequency) {
        String rest_id = twitterDataDao.queryRestIdByUsername(username);
        ConnectionUtils connectionUtils = new ConnectionUtils();
        HashMap<String, String> map = new HashMap<>();
        //鉴权头部信息
        map.put("x-guest-token", token);
        map.put("Authorization", "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA");
        String FixedURL = "https://twitter.com/i/api/graphql/p68c7OTFDZVMpkCA1-x3rg/UserTweets?variables=";
        String userId = "%7B%22userId%22%3A%22" + rest_id + "%22%2C";//rest_id
        String count = "%22count%22%3A" + onceGetNum.toString() + "%2C";//推文数，上限599(手动测的)
        String other =
                "%22withTweetQuoteCount%22%3Atrue%2C" + //推文引用计数
                        "%22includePromotedContent%22%3Atrue%2C" + //包括推广内容
                        "%22withSuperFollowsUserFields%22%3Afalse%2C" + //超级关注用户字段
                        "%22withUserResults%22%3Atrue%2C" + //带有用户信息
                        "%22withBirdwatchPivots%22%3Afalse%2C" + //
                        "%22withReactionsMetadata%22%3Afalse%2C" + //带有反应元数据
                        "%22withReactionsPerspective%22%3Afalse%2C" + //反应视角
                        "%22withSuperFollowsTweetFields%22%3Afalse%2C" + //使用超级关注推文字段
                        "%22withVoice%22%3Atrue%7D";//带语音
        String url = FixedURL + userId + count + other;
        String data = null;
        String botten_id = null;
        String start = null;
        if (frequency == -1){//一直获取

        }
        while (frequency!=0){
            try {
                System.out.println("请求地址："+url);
                data = connectionUtils.getJsonFromApiByHeader(url, map);
            } catch (Exception e) {
                e.printStackTrace();
            }
            botten_id = analyzeUserTweetsJSON(data);
            if (botten_id == null){
                break;
            }
            start = "%22cursor%22%3A%22"+ botten_id +"%3D%3D%22%2C";//推文起始位置
            url = FixedURL + userId + count + start + other;
            System.out.println("botten_id:"+botten_id);
            frequency--;
        }
        return "完成";
    }
}
