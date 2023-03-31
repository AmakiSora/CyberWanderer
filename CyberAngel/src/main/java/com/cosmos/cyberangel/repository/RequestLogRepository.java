package com.cosmos.cyberangel.repository;

import com.cosmos.cyberangel.entity.RequestLog;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

/**
 * RequestLog Repository
 */
public interface RequestLogRepository extends JpaRepository<RequestLog, Long> {

    List<RequestLog> findByStatus(Integer status, Pageable pageable);

    List<RequestLog> findByStatusAndIdNotIn(Integer status, Long[] ids, Pageable pageable);

}
