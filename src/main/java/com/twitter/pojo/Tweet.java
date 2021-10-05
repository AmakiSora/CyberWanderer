package com.twitter.pojo;

import lombok.Data;

@Data
public class Tweet {//推文
    private String username;//唯一用户名
    private String user_id;//唯一id
    private String created_at;//创建时间
    private String full_text;//推文内容
    private String tweet_id;//推文id
    private String tweet_img;//todo 推文图片
    private String tweet_display_type;//推文类型
//    EmphasizedPromotedTweet Tweet VerticalConversation
    private String tweet_type;//!推文类型
    private String quoted_tweet_id;//转推id
    private String quoted_name;//转推推文推特名
    private String quoted_username;//转推推文唯一用户名
    private String quoted_user_id;//转推推文唯一id
    private String quoted_created_at;//转推推文创建时间
    private String quoted_full_text;//转推推文内容
    private String delete;//!是否被删除
}
