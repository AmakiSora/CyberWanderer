package FakerData;

import FakerData.pojo.Product;
import Utils.ConnectionUtils;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import dao.FakerDataDao;
import dao.Utils.MybatisUtils;
import org.apache.ibatis.session.SqlSession;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class GetProduct {
    public static void get(int i) throws Exception {
        int a = 0;
        String fakeURL = "";
        List<String> faker = new ArrayList<>();
        faker.add("https://fakercloud.com/api/v1/schema/RSPocGhW?apiKey=ohKaa1CF&rows=100");//00
        faker.add("https://fakercloud.com/api/v1/schema/Z-rZFxDX?apiKey=nx9uRHw9&rows=100");//01
        faker.add("https://fakercloud.com/api/v1/schema/fHQcEooI?apiKey=o319LEFD&rows=100");//02
        faker.add("https://fakercloud.com/api/v1/schema/g0XnLD2s?apiKey=0DhyG1m7&rows=100");//03
        faker.add("https://fakercloud.com/api/v1/schema/Sv5DNQlR?apiKey=eDWoI1TD&rows=100");//04
        faker.add("https://fakercloud.com/api/v1/schema/0ibImtAQ?apiKey=RmELk4dc&rows=100");//07
        fakeURL = faker.get(0);
        for (int j = 0; j < i; j++) {
            if (get(fakeURL).equals("无了")){
                System.out.println("下一个");
                a++;
                if (a>=faker.size()){
                    System.out.println("无了");
                    return;
                }
                fakeURL = faker.get(a);
            }
        }
    }
    public static String get(String URL) throws Exception {
        String a = ConnectionUtils.CatchApi.getJsonFromApi(URL);
        JSONObject json = (JSONObject) JSON.parse(a);
        List<JSONObject> list = (List<JSONObject>) json.get("rows");
        if (list==null){
            return "无了";
        }
        SqlSession sqlSession = MybatisUtils.getSqlSession();
        FakerDataDao dao = sqlSession.getMapper(FakerDataDao.class);
        List<Product> lp = new ArrayList<>();
        for (JSONObject p:list){
            Product product = new Product();
            product.setName(p.getString("name"));
            product.setPrice((p.getString("price")));
            product.setDescription(p.getString("description"));
            product.setStock((Integer) p.get("stock"));
            product.setStatus((Integer) p.get("status"));
            product.setSell_time(new Date(p.getString("sell_time")));
            lp.add(product);
        }
        dao.insertProduct(lp);
        sqlSession.commit();
        sqlSession.close();
        return "";
    }
}
