package com.twitter.twitterDataDao;

import com.twitter.pojo.Tweet;
import com.twitter.pojo.TwitterUser;
import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;

import java.util.List;

@Mapper
@Repository
public interface TwitterDataDao {
    void insertTwitterUser(TwitterUser twitterUser);
    void insertTweet(Tweet tweet);
    void insertTweets(List<Tweet> tweets);
    List<String> queryImgUrlsByUsername(String username);
    String queryUserIdByUsername(String username);
}
