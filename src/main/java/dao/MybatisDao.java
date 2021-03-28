package dao;

import pojo.BiliBiliDynamic;

public interface MybatisDao {
    void insertBiliBiliDynamic(BiliBiliDynamic biliDynamic);
    BiliBiliDynamic selectBiliBiliDynamic();
}
