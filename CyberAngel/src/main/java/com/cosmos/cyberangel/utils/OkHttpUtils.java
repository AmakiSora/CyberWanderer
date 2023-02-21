package com.cosmos.cyberangel.utils;

import lombok.extern.slf4j.Slf4j;
import okhttp3.*;
import org.springframework.util.StringUtils;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.Proxy;
import java.util.Map;

/**
 * OkHttpUtils
 */
@Slf4j
public class OkHttpUtils {

    private static OkHttpClient client = new OkHttpClient.Builder().build();

    /**
     * setProxy
     */
    public static void setProxy(String hostname, int port) {
        if (StringUtils.hasText(hostname)) {
            log.info("OkHttp Proxy Address: {}:{}", hostname, port);
            Proxy proxy = new Proxy(Proxy.Type.HTTP, new InetSocketAddress(hostname, port));
            client = new OkHttpClient.Builder().proxy(proxy).build();
        } else {
            log.info("OkHttp proxy hostname does not exist");
        }
    }

    /**
     * get request
     */
    public static Response get(String url) throws IOException {
        return get(url, null);
    }

    public static Response get(String url, Map<String, String> headMap) throws IOException {
        Headers.Builder headBuilder = new Headers.Builder();
        if (headMap != null) {
            headMap.forEach(headBuilder::add);
        }
        Request request = new Request.Builder().url(url).headers(headBuilder.build()).build();
        return client.newCall(request).execute();

    }

    /**
     * post request
     */
    public static Response post(String url) throws IOException {
        return post(url, "", null);
    }

    public static Response post(String url, String content) throws IOException {
        return post(url, content, null);
    }

    public static Response post(String url, String content, Map<String, String> headMap) throws IOException {
        Headers.Builder headBuilder = new Headers.Builder();
        if (headMap != null) {
            headMap.forEach(headBuilder::add);
        }
        RequestBody body = RequestBody.create(content, MediaType.parse("application/json"));
        Request request = new Request.Builder().url(url).post(body).headers(headBuilder.build()).build();
        return client.newCall(request).execute();
    }

    /**
     * put request
     */
    public static Response put(String url) throws IOException {
        return put(url, "", null);
    }

    public static Response put(String url, String content) throws IOException {
        return put(url, content, null);
    }

    public static Response put(String url, String content, Map<String, String> headMap) throws IOException {
        Headers.Builder headBuilder = new Headers.Builder();
        if (headMap != null) {
            headMap.forEach(headBuilder::add);
        }
        RequestBody body = RequestBody.create(content, MediaType.parse("application/json"));
        Request request = new Request.Builder().url(url).put(body).headers(headBuilder.build()).build();
        return client.newCall(request).execute();
    }
}
