package com.cosmos.cyberangel.service;

import com.cosmos.cyberangel.entity.RequestLog;
import com.cosmos.cyberangel.repository.RequestLogRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.domain.Pageable;
import org.springframework.retry.annotation.Backoff;
import org.springframework.retry.annotation.Retryable;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Set;

/**
 * ParseService
 */
@Slf4j
@Service
public class ParseService {

    @Value("${ParseListSize:100}")
    private int ParseListSize;

    @Autowired
    private RequestLogRepository requestLogRepository;

    @Retryable(retryFor = {Exception.class},
            maxAttempts = Integer.MAX_VALUE,
            backoff = @Backoff(delay = 3000, multiplier = 1.5, maxDelay = 300000))
    public List<RequestLog> getParseList(Integer status, Set<Long> processingSet) {
        List<RequestLog> ids;
        Long[] excludeList = processingSet.toArray(new Long[0]);
        if (excludeList.length == 0) {
            ids = requestLogRepository.findByStatus(status, Pageable.ofSize(ParseListSize));
        } else {
            ids = requestLogRepository.findByStatusAndIdNotIn(status, excludeList, Pageable.ofSize(ParseListSize));
        }
        if (ids.isEmpty()) {
            log.info("<ParseJob> No data pending processing!");
            throw new NullPointerException("No data pending processing!");
        }
        return ids;
    }
}
