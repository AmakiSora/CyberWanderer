package com.fakerdata.pojo;

import lombok.Data;

import java.util.Date;

@Data
public class Person {
    private int id;
    private String last_name;//姓
    private String first_name;//名
    private String city;//城市
    private Date birth_date;//出生日期
    private String gender;//性别
    private String phone;//手机号
    private String email;//邮箱
}
