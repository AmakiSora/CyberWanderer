package com.twitter;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.twitter.pojo.Tweet;
import com.twitter.pojo.TwitterUser;
import com.twitter.twitterDataDao.TwitterDataDao;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class TwitterService {
    @Autowired
    private TwitterDataDao twitterDataDao;
    public String analyzeUserDetailJSON(String a){
        JSONObject Json = (JSONObject) JSON.parse(a);
        JSONObject userJson = (JSONObject) Json.getJSONObject("data").get("user");
        JSONObject resultJson = userJson.getJSONObject("result");
        JSONObject legacy_extended_profileJson = resultJson.getJSONObject("legacy_extended_profile");
        JSONObject legacyJson = resultJson.getJSONObject("legacy");
        JSONObject birthdateJson = legacy_extended_profileJson.getJSONObject("birthdate");

        TwitterUser user = new TwitterUser();

        try {//生日有可能为空
            String birthdate = birthdateJson.getString("year")+"-"+
                birthdateJson.getString("month")+"-"+
                birthdateJson.getString("day");
            //生日
            user.setBirthday(birthdate);

        }catch (Exception e){
            System.out.println(legacyJson.getString("name")+"未填写生日!!");
        }
        //名称
        user.setName(legacyJson.getString("name"));
        //唯一用户名
        user.setUsername(legacyJson.getString("screen_name"));
        //唯一id
        user.setUser_id(resultJson.getString("id"));
        //帐号创建时间
        user.setCreated_at(legacyJson.getString("created_at"));
        //简介
        user.setDescription(legacyJson.getString("description"));
        //展示链接
        user.setDisplay_url(legacyJson.getString("url"));
        //地点
        user.setLocation(legacyJson.getString("location"));
        //关注者
        user.setFollowers_count(legacyJson.getInteger("followers_count"));
        //正在关注
        user.setFriends_count(legacyJson.getInteger("friends_count"));

        twitterDataDao.insertTwitterUser(user);
        return "";
    }
    public String analyzeUserTweetsJSON(StringBuilder a){
        JSONObject json = JSONObject.parseObject(a.toString());
        JSONObject timelineJson = json.getJSONObject("data")
                .getJSONObject("user")
                .getJSONObject("result")
                .getJSONObject("timeline")
                .getJSONObject("timeline")
                ;
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
                        JSONObject itemContent = dd.getJSONObject("content").getJSONObject("itemContent");
                        tweet.setTweet_display_type(itemContent.getString("tweetDisplayType"));
                        JSONObject result = itemContent.getJSONObject("tweet_results").getJSONObject("result");
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
                        if (hashtags_List != null && !hashtags_List.isEmpty()){ //有标签
                            StringBuilder tag = new StringBuilder();
                            for (JSONObject h : hashtags_List) {
                                tag.append("#").append(h.getString("text"));
                            }
                            tweet.setTweet_hashtags(tag.toString());//推文标签
                        }

                        List<JSONObject> media_List = (List<JSONObject>) entities.get("media");
                        if (media_List != null && !media_List.isEmpty()){
                            StringBuilder media_urls = new StringBuilder();
                            for (JSONObject m : media_List) {
                                media_urls.append("|").append(m.getString("media_url_https"));
                            }
                            tweet.setTweet_media_urls(media_urls.toString());//推文图片地址
                            //todo 待完善
                        }

                        if (legacy.getBoolean("is_quote_status")) { //true为转推 false不是
                            tweet.setTweet_type("Retweeted");//推文类型!!!
                            tweet.setQuoted_tweet_id(legacy.getString("quoted_status_id_str"));
                            JSONObject quotedResult = result.getJSONObject("quoted_status_result").getJSONObject("result");
                            JSONObject user_results = quotedResult.getJSONObject("core")
                                    .getJSONObject("user_results")
                                    .getJSONObject("result");
                            tweet.setQuoted_user_id(user_results.getString("id"));//转推人唯一id
                            JSONObject quoted_user_legacy = user_results.getJSONObject("legacy");
                            tweet.setQuoted_name(quoted_user_legacy.getString("name"));//转推人名称
                            tweet.setQuoted_username(quoted_user_legacy.getString("screen_name"));//转推人唯一用户名

                            JSONObject quoted_tweet_legacy = quotedResult.getJSONObject("legacy");
                            tweet.setQuoted_tweet_id(quoted_tweet_legacy.getString("id_str"));
                            tweet.setQuoted_created_at(quoted_tweet_legacy.getString("created_at"));
                            tweet.setQuoted_full_text(quoted_tweet_legacy.getString("full_text"));
//                            tweet.setQuoted_tweet_img();
                            //todo 完成转推的内容
                        } else if (entryId.matches("^homeConversation-[0-9-a-zA-Z]*")) { //连续推文
                            System.out.println("连续推文");
                        } else if (entryId.matches("^promotedTweet-[0-9-a-zA-Z]*")) { //推广推文(广告)
//                        System.out.println("推广推文,暂时不处理");
                        } else if (entryId.matches("^whoToFollow-[0-9-a-zA-Z]*")) { //推荐关注
//                        System.out.println("推荐关注,暂时不处理");
                        } else if (entryId.matches("^cursor-top-[0-9-a-zA-Z]*")) { //光标顶部
//                        System.out.println("光标顶部,暂时不处理");
                        } else if (entryId.matches("^cursor-bottom-[0-9-a-zA-Z]*")) { //光标底部
//                        System.out.println("光标底部,暂时不处理");
                        }

                        tweets.add(tweet);
                    }
                }
            }else if ("TimelinePinEntry".equals(d.get("type"))){//置顶推文
//                System.out.println("TimelinePinEntry,暂时不处理");
            }
        }
        return "";
    }
}
