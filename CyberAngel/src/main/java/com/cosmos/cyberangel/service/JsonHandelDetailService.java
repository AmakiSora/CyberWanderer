package com.cosmos.cyberangel.service;

import com.alibaba.fastjson2.JSONArray;
import com.alibaba.fastjson2.JSONObject;
import com.cosmos.cyberangel.entity.JsonHandelDetail;
import com.cosmos.cyberangel.repository.JsonHandelDetailRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
/**
 * JsonHandelDetailService
 */
@Slf4j
@Service
public class JsonHandelDetailService {
    @Autowired
    private JsonHandelDetailRepository jsonHandelDetailRepository;

    public void s(String handelMethod){
        JsonHandelDetail detail = jsonHandelDetailRepository.getJsonHandelDetailByHandelMethod(handelMethod);
//        detail.getHandelDetail();
    }
    public void parseJson(JSONObject json) {
        for (String key : json.keySet()) {
            Object value = json.get(key);
            if (value instanceof JSONObject) {
                parseJson((JSONObject) value);
            } else if (value instanceof JSONArray array) {
                for (int i = 0; i < array.size(); i++) {
                    parseJson(array.getJSONObject(i));
                }
            } else {
                System.out.println(key + ":" + value);
            }
        }
    }
}
