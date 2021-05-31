package FakerData;

import FakerData.pojo.Person;
import FakerData.pojo.Product;
import Utils.ConnectionUtils;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import dao.FakerDataDao;
import dao.Utils.MybatisUtils;
import org.apache.ibatis.session.SqlSession;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class GetProduct {
    public static void get() throws Exception {
        String fakeURL = "https://fakercloud.com/api/v1/schema/0ibImtAQ?apiKey=RmELk4dc&rows=100";//07
//        String fakeURL = "";
//        String fakeURL = "";
//        String fakeURL = "";
//        String fakeURL = "";
//        String fakeURL = "";
        String a = ConnectionUtils.CatchApi.getJsonFromApi(fakeURL);
        JSONObject json = (JSONObject) JSON.parse(a);
        List<JSONObject> list = (List<JSONObject>) json.get("rows");
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
    }
    public static void get(int i) throws Exception {
        for (int j = 0; j < i; j++) {
            get();
        }
    }
}
