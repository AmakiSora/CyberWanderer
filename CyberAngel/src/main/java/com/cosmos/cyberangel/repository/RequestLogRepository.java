package com.cosmos.cyberangel.repository;

import com.cosmos.cyberangel.entity.RequestLog;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * RequestLog Repository
 */
public interface RequestLogRepository extends JpaRepository<RequestLog, Long> {
}
