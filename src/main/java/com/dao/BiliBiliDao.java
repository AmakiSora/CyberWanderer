package com.dao;

import com.bilibili.pojo.BiliBiliDynamic;
import com.bilibili.pojo.BiliBiliUser;
import org.springframework.stereotype.Repository;

@Repository
public interface BiliBiliDao {
    void insertBiliBiliDynamic(BiliBiliDynamic biliDynamic);
    void insertBiliBiliUser(BiliBiliUser biliUser);
}
