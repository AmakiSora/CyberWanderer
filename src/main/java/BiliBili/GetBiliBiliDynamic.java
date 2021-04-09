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
        //未登录动态
        String unlogin_dynamics = "unlogin_dynamics?fake_uid=156789&hot_offset=0";
        //用户动态
        String login_dynamics = "dynamic_new?uid=35274219&type_list=268435455&from=weball&platform=web";
        //UP主动态
        String host_uid = "11073";//用户id
        String space_history = "space_history?host_uid="+host_uid+"&offset_dynamic_id=0";//UP主动态
        getDynamic(space_history);
    }
    public static void getDynamic(String parameter) throws Exception {
        String urlHeader = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/";
        String url = urlHeader+parameter;
        String a = ConnectionUtils.CatchApi.getJsonFromApi(url);
        JSONObject json = (JSONObject) JSON.parse(a);
        List<JSONObject> list = (List<JSONObject>) json.getJSONObject("data").get("cards");
        SqlSession sqlSession = MybatisUtils.getSqlSession();
        MybatisDao dao = sqlSession.getMapper(MybatisDao.class);
        BiliBiliDynamic biliDynamic = new BiliBiliDynamic();
        BiliBiliUser biliUser = new BiliBiliUser();
        for (JSONObject d:list){
            JSONObject card = d.getJSONObject("card");
            JSONObject desc = d.getJSONObject("desc");
            JSONObject userInfo = desc.getJSONObject("user_profile").getJSONObject("info");
            //type 1:动态转发 2:自己发表的动态 4:自己发表的无图片动态 8:视频投稿 512:动漫影剧 4308:直播 64:专栏
            if(d.getJSONObject("desc").get("type").equals(1)){//1:动态转发
                //动态id
                biliDynamic.setNO(desc.getLong("dynamic_id"));
                //用户id
                biliDynamic.setId(userInfo.getString("uid"));
                //用户名
                biliDynamic.setName(userInfo.getString("uname"));
                //动态类型
                biliDynamic.setType("1");
                //动态时间
                biliDynamic.setUploadTime(new Timestamp(desc.getLong("timestamp")*1000));
                //动态内容
                biliDynamic.setContent(card.getJSONObject("item").getString("content"));
            } else if (d.getJSONObject("desc").get("type").equals(2)){//2:自己发表的动态
                biliDynamic.setId((String) userInfo.get("uid"));
                biliDynamic.setName(userInfo.getString("uname"));
                biliDynamic.setContent(card.getJSONObject("item").getString("description"));
                biliDynamic.setNO(desc.getLong("dynamic_id"));
            } else if (d.getJSONObject("desc").get("type").equals(4)){//4:自己发表的无图片动态
                biliDynamic.setNO(desc.getLong("dynamic_id"));
                biliDynamic.setId((String) userInfo.get("uid"));
                biliDynamic.setName(userInfo.getString("uname"));
                biliDynamic.setContent(card.getJSONObject("item").getString("content"));
            } else if (d.getJSONObject("desc").get("type").equals(8)){//8:视频投稿
                biliDynamic.setNO(desc.getLong("dynamic_id"));
                biliDynamic.setId((String) userInfo.get("uid"));
                biliDynamic.setName(userInfo.getString("uname"));
                biliDynamic.setContent(card.getString("dynamic"));

            } else if (d.getJSONObject("desc").get("type").equals(512)){//512:动漫影剧

            } else if (d.getJSONObject("desc").get("type").equals(64)){//64:专栏

            } else if (d.getJSONObject("desc").get("type").equals(4308)){//4308:直播

            }

            String avatarURL = (String) userInfo.get("face");


            dao.insertBiliBiliDynamic(biliDynamic);
            dao.insertBiliBiliUser(biliUser);
        }
        sqlSession.commit();
        sqlSession.close();
    }
}
