package com.twitter;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.twitter.pojo.TwitterUser;
import com.twitter.twitterDataDao.TwitterDataDao;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class TwitterService {
    @Autowired
    private TwitterDataDao twitterDataDao;
    public String AnalyzeUserDetailJSON(String a){
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
    public String AnalyzeUserTweetsJSON(String a){
        return "";
    }
}
