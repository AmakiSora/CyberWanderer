package com.twitter.twitterDataDao;

import com.twitter.pojo.TweetJSON;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface TwitterMongoDao extends MongoRepository<TweetJSON,String> {
}
