package FakerData;

import BiliBili.pojo.BiliBiliDynamic;
import BiliBili.pojo.BiliBiliUser;
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
    public static void get() throws Exception {
//        String fakeURL = "https://fakercloud.com/api/v1/schema/qNrDBAam?apiKey=nx9uRHw9&rows=100";
//        String fakeURL = "https://fakercloud.com/api/v1/schema/62Jp0CsI?apiKey=o319LEFD&rows=100";
//        String fakeURL = "https://fakercloud.com/api/v1/schema/BFMuRdr6?apiKey=ohKaa1CF&rows=100";
//        String fakeURL = "https://fakercloud.com/api/v1/schema/kmkxMwsm?apiKey=0DhyG1m7&rows=100";
//        String fakeURL = "https://fakercloud.com/api/v1/schema/NDr0OhJN?apiKey=eDWoI1TD&rows=100";
        String fakeURL = "https://fakercloud.com/api/v1/schema/7YA9l2zJ?apiKey=K9ekRKaB&rows=100";//05
        String a = ConnectionUtils.CatchApi.getJsonFromApi(fakeURL);
        JSONObject json = (JSONObject) JSON.parse(a);
        List<JSONObject> list = (List<JSONObject>) json.get("rows");
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
//            dao.insertPerson(person);
            lp.add(person);
        }
        dao.insertPersons(lp);
        sqlSession.commit();
        sqlSession.close();
    }
    public static void get(int i) throws Exception {
        for (int j = 0; j < i; j++) {
            get();
        }
    }
}
