package BiliBili.pojo;

import lombok.Data;

import java.sql.Timestamp;

@Data
public class BiliBiliDynamic {
    private Long NO;//动态id
    private String id;//用户id
    private String name;//用户名
    private String type;//动态类型
    private Timestamp uploadTime;//动态时间戳
    private String content;//动态内容
    private String imgURL;//动态图片URL
}
