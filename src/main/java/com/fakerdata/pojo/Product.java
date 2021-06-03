package com.fakerdata.pojo;

import lombok.Data;

import java.util.Date;

@Data
public class Product {
    private int id;
    private String name;//商品名
    private String price;//价格
    private String description;//描述
    private int stock;//库存
    private int status;//状态
    private Date sell_time;//上架时间
}
