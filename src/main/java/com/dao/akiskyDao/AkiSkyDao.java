package com.dao.akiskyDao;

import com.bilibili.pojo.BiliBiliDynamic;
import com.bilibili.pojo.BiliBiliUser;
import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;
@Mapper
@Repository
public interface AkiSkyDao {
    void insertBiliBiliDynamic(BiliBiliDynamic biliDynamic);
    void insertBiliBiliUser(BiliBiliUser biliUser);
}
