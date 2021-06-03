package com.bilibili;

import com.bilibili.pojo.BiliBiliUser;
import com.utils.ConnectionUtils;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.bilibili.pojo.BiliBiliDynamic;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.sql.Timestamp;
import java.util.List;

/**
 * 获取霹雳霹雳动态类
 */
@Service
public class GetBiliBiliDynamic {
    @Autowired
    private ConnectionUtils connectionUtils;

    public void GetBiliBiliDynamic() throws Exception {
        getSomeDynamic(20);
//        getUserDynamic(100,10);
//        getUserDynamic(101,106,10,100);
        //用户动态
//        String login_dynamics = "dynamic_new?uid=35274219&type_list=268435455&from=weball&platform=web";

    }

    /**
     * 获取未登录的动态
     * @param total 获取多少次
     * @throws Exception
     */
    public void getSomeDynamic(int total) throws Exception {
        String xxx_offset = "0";
        String unlogin_dynamics = "unlogin_dynamics?fake_uid=961737&hot_offset="+xxx_offset;
        for (int i = 0; i < total; i++) {
            xxx_offset = getDynamic(unlogin_dynamics);
            System.out.println(xxx_offset);
            if (xxx_offset.equals("无了")){
                return;
            }
            unlogin_dynamics = "unlogin_dynamics?fake_uid=15789&hot_offset="+xxx_offset;
        }
    }

    /**
     * 获取某个up的动态
     * @param host_uid up主id
     * @param up_sum 获取多少次
     * @throws Exception
     */
    public void getUserDynamic(int host_uid,int up_sum) throws Exception {
        String xxx_offset = "0";
        String space_history = "space_history?host_uid="+host_uid+"&offset_dynamic_id="+xxx_offset;//UP主动态
        for (int i = 0; i < up_sum; i++) {//总循环次数
            xxx_offset = getDynamic(space_history);
            System.out.println(xxx_offset);
            if (xxx_offset.equals("无了")){
                return;
            }
            space_history = "space_history?host_uid="+host_uid+"&offset_dynamic_id="+xxx_offset;
        }
    }
    /**
     * 获取某范围的up动态
     * @param host_uid 起始up主id
     * @param last_uid 最后一位up主id
     * @param up_sum 每个up主最多获取多少次
     * @param total 总共获取多少次
     * @throws Exception
     */
    public void getUserDynamic(int host_uid,int last_uid,int up_sum,int total) throws Exception {
        String xxx_offset = "0";
        int sum = 0;
        String space_history = "space_history?host_uid="+host_uid+"&offset_dynamic_id="+xxx_offset;//UP主动态
        for (int i = 0; i < total; i++) {//总循环次数
            if (sum == up_sum){
                xxx_offset = "0";
                host_uid = host_uid+1;
                sum = 0;
            }
            xxx_offset = getDynamic(space_history);
            System.out.println(xxx_offset);
            if (xxx_offset.equals("无了")){
                xxx_offset = "0";
                host_uid = host_uid+1;
                if (host_uid==last_uid){
                    return;
                }
            }
            sum++;
            space_history = "space_history?host_uid="+host_uid+"&offset_dynamic_id="+xxx_offset;
        }
    }

    /**
     * 获取b站动态，一次最多6条
     * @param parameter url后面的参数
     * @return 返回最后一条动态的id,如果没有查询到动态则返回"无了"
     * @throws Exception
     */
    public String getDynamic(String parameter) throws Exception {
        String urlHeader = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/";
        String url = urlHeader+parameter;
        String a = connectionUtils.getJsonFromApi(url);
        JSONObject json = (JSONObject) JSON.parse(a);
        List<JSONObject> list = (List<JSONObject>) json.getJSONObject("data").get("cards");
        if (list==null){
            return "无了";
        }
//        SqlSession sqlSession = MybatisUtils.getSqlSession();
//        MybatisDao dao = sqlSession.getMapper(MybatisDao.class);
        BiliBiliDynamic biliDynamic = new BiliBiliDynamic();
        BiliBiliUser biliUser = new BiliBiliUser();
        String dynamic_id = "";
        for (JSONObject d:list){
            JSONObject card = d.getJSONObject("card");
            JSONObject desc = d.getJSONObject("desc");
            JSONObject userInfo = desc.getJSONObject("user_profile").getJSONObject("info");
            //type 1:动态转发 2:自己发表的动态 4:自己发表的无图片动态 8:视频投稿 512:动漫影剧 4308:直播 64:专栏
            dynamic_id = desc.getLong("dynamic_id").toString();
            biliDynamic.setNO(desc.getLong("dynamic_id"));//动态id
            biliDynamic.setUploadTime(new Timestamp(desc.getLong("timestamp")*1000));//动态时间
            biliDynamic.setId(userInfo.getString("uid"));//用户id
            biliDynamic.setName(userInfo.getString("uname"));//用户名
            if(d.getJSONObject("desc").get("type").equals(1)){//1:动态转发
                biliDynamic.setType("1");//动态类型
                biliDynamic.setContent(card.getJSONObject("item").getString("content"));//动态内容
            } else if (d.getJSONObject("desc").get("type").equals(2)){//2:自己发表的动态
                biliDynamic.setType("2");//动态类型
                biliDynamic.setContent(card.getJSONObject("item").getString("description"));//动态内容
            } else if (d.getJSONObject("desc").get("type").equals(4)){//4:自己发表的无图片动态
                biliDynamic.setType("4");//动态类型
                biliDynamic.setContent(card.getJSONObject("item").getString("content"));//动态内容
            } else if (d.getJSONObject("desc").get("type").equals(8)){//8:视频投稿
                biliDynamic.setType("8");//动态类型
                biliDynamic.setContent(card.getString("dynamic"));
            } else if (d.getJSONObject("desc").get("type").equals(512)){//512:动漫影剧
                biliDynamic.setType("512");//动态类型
            } else if (d.getJSONObject("desc").get("type").equals(64)){//64:专栏
                biliDynamic.setType("64");//动态类型
            } else if (d.getJSONObject("desc").get("type").equals(4308)){//4308:直播
                biliDynamic.setType("4308");//动态类型
            }

            String avatarURL = (String) userInfo.get("face");
            biliUser.setAvatarURL(avatarURL);
            biliUser.setId(userInfo.getString("uid"));
            biliUser.setName(userInfo.getString("uname"));
//            dao.insertBiliBiliDynamic(biliDynamic);
//            dao.insertBiliBiliUser(biliUser);
        }
//        sqlSession.commit();
//        sqlSession.close();
        return dynamic_id;
    }
}
