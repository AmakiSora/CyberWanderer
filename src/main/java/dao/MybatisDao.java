package dao;

import BiliBili.pojo.BiliBiliDynamic;
import BiliBili.pojo.BiliBiliUser;

public interface MybatisDao {
    void insertBiliBiliDynamic(BiliBiliDynamic biliDynamic);
    void insertBiliBiliUser(BiliBiliUser biliUser);
}
