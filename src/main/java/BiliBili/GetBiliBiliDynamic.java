package BiliBili;

import BiliBili.pojo.BiliBiliUser;
import Utils.ConnectionUtils;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import dao.MybatisDao;
import dao.Utils.MybatisUtils;
import org.apache.ibatis.session.SqlSession;
import BiliBili.pojo.BiliBiliDynamic;

import java.sql.Timestamp;
import java.util.List;

public class GetBiliBiliDynamic {
    public static void GetBiliBiliDynamic() throws Exception {
        String xxx_offset = "0";
        //未登录动态
        String unlogin_dynamics = "unlogin_dynamics?fake_uid=13789&hot_offset="+xxx_offset;
        //用户动态
        String login_dynamics = "dynamic_new?uid=35274219&type_list=268435455&from=weball&platform=web";
        //UP主动态
        String host_uid = "6";//用户id
        String space_history = "space_history?host_uid="+host_uid+"&offset_dynamic_id="+xxx_offset;//UP主动态
//        for (int i = 0; i < 3; i++) {
//        xxx_offset = getDynamic(unlogin_dynamics);
//        System.out.println(xxx_offset);
//        unlogin_dynamics = "unlogin_dynamics?fake_uid=15789&hot_offset="+xxx_offset;
//        }
        for (int i = 0; i < 5; i++) {
        xxx_offset = getDynamic(space_history);
        System.out.println(xxx_offset);
        space_history = "space_history?host_uid="+host_uid+"&offset_dynamic_id="+xxx_offset;
        }
    }
    public static String getDynamic(String parameter) throws Exception {
        String urlHeader = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/";
        String url = urlHeader+parameter;
        String a = ConnectionUtils.CatchApi.getJsonFromApi(url);
        JSONObject json = (JSONObject) JSON.parse(a);
        List<JSONObject> list = (List<JSONObject>) json.getJSONObject("data").get("cards");
        SqlSession sqlSession = MybatisUtils.getSqlSession();
        MybatisDao dao = sqlSession.getMapper(MybatisDao.class);
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
            dao.insertBiliBiliDynamic(biliDynamic);
            dao.insertBiliBiliUser(biliUser);
        }
        sqlSession.commit();
        sqlSession.close();
        return dynamic_id;
    }
}
