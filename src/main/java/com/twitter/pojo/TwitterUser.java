package com.twitter.pojo;

import lombok.Data;


@Data
public class TwitterUser {//推特帐号
    private String name;//名称
    private String username;//唯一用户名
    private String user_id;//唯一id
    private String created_at;//帐号创建时间
    private String birthday;//生日
    private String description;//简介
    private int friends_count;//正在关注
    private int followers_count;//关注者
    private String location;//地点
    private String display_url;//展示链接
}
