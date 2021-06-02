package FakerData;

import FakerData.pojo.Person;
import Utils.ConnectionUtils;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import dao.FakerDataDao;
import dao.Utils.MybatisUtils;
import org.apache.ibatis.session.SqlSession;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class GetPersons {
    public static void get(int i) throws Exception {
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
        dao.insertPersons(lp);
        sqlSession.commit();
        sqlSession.close();
        return "";
    }
}
