package com.cosmos.cyberangel.config;

import com.cosmos.cyberangel.utils.OkHttpUtils;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * OkHttpConfig
 */
@Slf4j
@Configuration
public class OkHttpConfig {

    /**
     * Proxy hostname
     */
    @Value("${okhttp.proxy.hostname:}")
    private String hostname;

    /**
     * Proxy port
     */
    @Value("${okhttp.proxy.port:0}")
    private int port;

    /**
     * OkHttp init
     */
    @Bean
    public void initStatic() {
        OkHttpUtils.setProxy(hostname, port);
    }
}
