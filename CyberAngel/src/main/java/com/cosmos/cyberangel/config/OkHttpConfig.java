package com.cosmos.cyberangel.config;

import com.cosmos.cyberangel.utils.OkHttpUtils;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * OkHttp配置
 */
@Slf4j
@Configuration
public class OkHttpConfig {

    @Value("${okhttp.proxy.hostname:}")
    private String hostname;

    @Value("${okhttp.proxy.port:0}")
    private int port;

    @Bean
    public void initStatic() {
        OkHttpUtils.setProxy(hostname, port);
    }
}
