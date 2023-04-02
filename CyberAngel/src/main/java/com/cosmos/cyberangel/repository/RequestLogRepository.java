package com.cosmos.cyberangel.repository;

import com.cosmos.cyberangel.entity.RequestLog;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

/**
 * RequestLog Repository
 */
public interface RequestLogRepository extends JpaRepository<RequestLog, Long> {

    List<RequestLog> findByStatus(Integer status, Pageable pageable);

    List<RequestLog> findByStatusAndIdNotIn(Integer status, Long[] ids, Pageable pageable);

    @Modifying
    @Query("update RequestLog l set l.status = :status where l.id = :id")
    int updateStatusById(@Param("id") Long id, @Param("status") Integer status);
}
