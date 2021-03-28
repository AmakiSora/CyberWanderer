import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import dao.MybatisDao;
import dao.Utils.MybatisUtils;
import org.apache.ibatis.session.SqlSession;
import pojo.BiliBiliDynamic;

import java.io.IOException;
import java.util.List;

public class BiliBiliDynamicHandle {
    public static void getDynamic() throws Exception {
        String url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/unlogin_dynamics";
        String a = Utils.CatchApi.getJsonFromApi(url);
        JSONObject json = (JSONObject) JSON.parse(a);
        List<JSONObject> lj = (List<JSONObject>) json.getJSONObject("data").get("cards");
        SqlSession sqlSession = MybatisUtils.getSqlSession();
        MybatisDao dao = sqlSession.getMapper(MybatisDao.class);
        BiliBiliDynamic biliDynamic = new BiliBiliDynamic();
        for (JSONObject d:lj){
            String name = (String) d.getJSONObject("card").getJSONObject("user").get("name");
            String description = (String) d.getJSONObject("card").getJSONObject("item").get("description");
            System.out.println(name);
            System.out.println(description);
            biliDynamic.setName(name);
            biliDynamic.setDescription(description);
            dao.insertBiliBiliDynamic(biliDynamic);
        }
        sqlSession.commit();
        sqlSession.close();
    }
}
