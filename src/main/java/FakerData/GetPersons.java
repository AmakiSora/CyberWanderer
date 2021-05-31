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

import java.util.Date;
import java.util.List;

public class GetPersons {
    public static void get() throws Exception {
        String fakeURL = "https://fakercloud.com/api/v1/schema/62Jp0CsI?apiKey=o319LEFD&rows=100";
        String a = ConnectionUtils.CatchApi.getJsonFromApi(fakeURL);
        JSONObject json = (JSONObject) JSON.parse(a);
        List<JSONObject> list = (List<JSONObject>) json.get("rows");
        SqlSession sqlSession = MybatisUtils.getSqlSession();
        FakerDataDao dao = sqlSession.getMapper(FakerDataDao.class);
        Person person = new Person();
        for (JSONObject p:list){
            person.setLast_name(p.getString("last_name"));
            person.setFirst_name(p.getString("first_name"));
            person.setCity(p.getString("city"));
            person.setBirth_date(new Date(p.getString("birth_date")));
            person.setGender(p.getString("gender"));
            person.setPhone(p.getString("phone"));
            person.setEmail(p.getString("email"));
            dao.insertPerson(person);
        }
        sqlSession.commit();
        sqlSession.close();
    }
}
