package com.twitter.service;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.twitter.pojo.TwitterUser;
import com.twitter.twitterDataDao.TwitterDataDao;
import com.utils.ConnectionUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.HashMap;

@Service
public class TwitterUserService {
    @Autowired
    TwitterDataDao twitterDataDao;
    public String getUserIdByUsername(String username){//查user_id 根据username
        return twitterDataDao.queryUserIdByUsername(username);
    }
    public String getRestIdByUsername(String username){//查rest_id 根据username
        return twitterDataDao.queryRestIdByUsername(username);
    }
    public String analyzeUserInfoJSON(String a,boolean toDB){
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
        //唯一id,rest_id
        user.setRest_id(resultJson.getString("rest_id"));
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

        if (toDB){
            twitterDataDao.insertTwitterUser(user);
        }else {
            System.out.println(user);
        }
        return user.toString();
    }
    public String autoGetUserDetail(String token,String username,boolean toDB){
        HashMap<String, String> map = new HashMap<>();
        //鉴权头部信息
        map.put("Host", "twitter.com");
        map.put("x-guest-token", token);
        map.put("Authorization", "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA");
        String FixedURL = "https://twitter.com/i/api/graphql/cYsDlVss-qimNYmNlb6inw/UserByScreenName?variables=";
        String p = "%7B%22screen_name%22%3A%22"+ username +"%22%2C" +
                "%22withSafetyModeUserFields%22%3Atrue%2C" +
                "%22withSuperFollowsUserFields%22%3Afalse%7D";
        String url = FixedURL + p;
        try {
            String json = new ConnectionUtils().getJsonFromApiByHeader(url, map);
            analyzeUserInfoJSON(json,toDB);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return "成功";
    }

}
