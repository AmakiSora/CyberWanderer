package com.twitter.twitterDataDao;

import com.twitter.pojo.TwitterUser;
import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;

@Mapper
@Repository
public interface TwitterDataDao {
    void insertTwitterUser(TwitterUser twitterUser);
}
