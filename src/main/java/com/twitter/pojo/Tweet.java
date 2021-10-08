package com.twitter.pojo;

import lombok.Data;

/**
 * 推文
 * !!!为自定义字段,其他字段均取自json
 */
@Data
public class Tweet {
    private String name;//名称
    private String username;//唯一用户名
    private String user_id;//唯一id
    private String created_at;//创建时间
    private String full_text;//推文内容
    private String tweet_id;//推文id
    private String tweet_media_urls;//推文媒体地址(主要是图片)
    private String tweet_hashtags;//推文标签
    private String tweet_urls;//推文扩展地址
    private String tweet_type;//推文类型!!!
    private String delete;//是否被删除!!!

    private String quoted_tweet_id;//转推id,以下全部另存

//    private String quoted_name;//转推推文推特名称
//    private String quoted_username;//转推推文唯一用户名
//    private String quoted_user_id;//转推推文唯一id
//    private String quoted_created_at;//转推推文创建时间
//    private String quoted_full_text;//转推推文内容
//    private String quoted_tweet_img;//转推推文图片
}
