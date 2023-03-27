package com.cosmos.cyberangel.service;

import com.cosmos.cyberangel.repository.RequestLogRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.retry.annotation.Backoff;
import org.springframework.retry.annotation.Retryable;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * ParseService
 */
@Slf4j
@Service
public class ParseService {

    @Autowired
    private RequestLogRepository requestLogRepository;

    @Retryable(retryFor = {Exception.class},
            maxAttempts = Integer.MAX_VALUE,
            backoff = @Backoff(delay = 3000, multiplier = 1.5, maxDelay = 300000))
    public void getParseList() {
        String now = LocalDateTime.now().format(DateTimeFormatter.ofPattern("hh:mm:ss"));
        log.info("getParseList,time:[{}]", now);
        throw new NullPointerException("null");
    }
}
