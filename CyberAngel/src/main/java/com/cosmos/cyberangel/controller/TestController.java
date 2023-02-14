package com.cosmos.cyberangel.controller;

import com.cosmos.cyberangel.utils.OkHttpUtils;
import lombok.extern.slf4j.Slf4j;
import okhttp3.Response;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * test
 */
@Slf4j
@RestController
@RequestMapping("/test")
public class TestController {
    /**
     * Simple get request
     */
    @GetMapping("/get")
    public String get(@RequestParam String url) {
        try {
            Response response = OkHttpUtils.get(url);
            assert response.body() != null;
            String data = response.body().string();
            log.info(data);
            return data;
        } catch (Exception e) {
            log.error("error", e);
            return e.toString();
        }
    }

}
