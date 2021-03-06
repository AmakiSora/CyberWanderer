package com.fakerdata;

import com.fakerdata.pojo.Person;
import com.utils.ConnectionUtils;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.dao.fakerdataDao.FakerDataDao;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;
@Service
public class GetPersons {
    @Autowired
    private ConnectionUtils connectionUtils;
    @Autowired
    private FakerDataDao fakerDataDao;
    public String get(int i) throws Exception {
        int a = 0;
        String fakeURL = "";
        List<String> faker = new ArrayList<>();
        faker.add("https://fakercloud.com/api/v1/schema/BFMuRdr6?apiKey=ohKaa1CF&rows=100");//00
        faker.add("https://fakercloud.com/api/v1/schema/qNrDBAam?apiKey=nx9uRHw9&rows=100");//01
        faker.add("https://fakercloud.com/api/v1/schema/62Jp0CsI?apiKey=o319LEFD&rows=100");//02
        faker.add("https://fakercloud.com/api/v1/schema/kmkxMwsm?apiKey=0DhyG1m7&rows=100");//03
        faker.add("https://fakercloud.com/api/v1/schema/NDr0OhJN?apiKey=eDWoI1TD&rows=100");//04
        faker.add("https://fakercloud.com/api/v1/schema/7YA9l2zJ?apiKey=K9ekRKaB&rows=100");//05
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
        List<Person> lp = new ArrayList<>();
        for (JSONObject p:list){
            Person person = new Person();
            person.setLast_name(p.getString("last_name"));
            person.setFirst_name(p.getString("first_name"));
            person.setCity(p.getString("city"));
            person.setBirth_date(new Date(p.getString("birth_date")));
            person.setGender(p.getString("gender"));
            person.setPhone(p.getString("phone"));
            person.setEmail(p.getString("email"));
            lp.add(person);
        }
        fakerDataDao.insertPersons(lp);
        return "";
    }
}
