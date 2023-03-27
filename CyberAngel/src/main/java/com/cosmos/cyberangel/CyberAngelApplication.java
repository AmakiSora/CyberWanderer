package com.cosmos.cyberangel;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.retry.annotation.EnableRetry;

@EnableRetry
@SpringBootApplication
public class CyberAngelApplication {

    public static void main(String[] args) {
        SpringApplication.run(CyberAngelApplication.class, args);
    }

}
