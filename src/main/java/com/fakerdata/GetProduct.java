package com.fakerdata;

import com.fakerdata.pojo.Product;
import com.utils.ConnectionUtils;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.dao.FakerDataDao;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;
@Service
public class GetProduct {
    @Autowired
    private ConnectionUtils connectionUtils;
    @Autowired
    private FakerDataDao fakerDataDao;
    public String get(int i) throws Exception {
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
                    return "没有次数了";
                }
                fakeURL = faker.get(a);
            }
        }
        return "完成";
    }
    public String get(String URL) throws Exception {
        String a = connectionUtils.getJsonFromApi(URL);
        JSONObject json = (JSONObject) JSON.parse(a);
        List<JSONObject> list = (List<JSONObject>) json.get("rows");
        if (list==null){
            return "无了";
        }
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
        fakerDataDao.insertProduct(lp);
        return "";
    }
}
