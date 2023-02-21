package com.cosmos.cyberangel.service;

import com.cosmos.cyberangel.utils.OkHttpUtils;
import okhttp3.Response;
import org.jetbrains.annotations.NotNull;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

/**
 * Request Service
 */
@Service
public class RequestService {

    public String checkUrl(String url) {
        if (!StringUtils.hasText(url)) {
            throw new IllegalArgumentException("Please enter the correct url!");
        }
        if (!(url.startsWith("http://") || url.startsWith("https://"))) {
            url = "http://" + url;
        }
        return url;
    }

    @NotNull
    private void checkResponse(Response response) throws Exception {
        if (response == null) {
            throw new Exception("Response is null!");
        }
        int code = response.code();
        if (!response.isSuccessful()) {
            throw new Exception("Response error! code:" + code);
        }
        if (response.body() == null) {
            throw new Exception("Response body is null! code:" + code);
        }
    }

    public String get(String url) throws Exception {
        Response response = OkHttpUtils.get(url);
        checkResponse(response);
        return response.body().string();
    }

    public String post(String url, String json) throws Exception {
        Response response = OkHttpUtils.post(url, json);
        checkResponse(response);
        return response.body().string();
    }

    public String put(String url, String json) throws Exception {
        Response response = OkHttpUtils.put(url, json);
        checkResponse(response);
        return response.body().string();
    }
}
