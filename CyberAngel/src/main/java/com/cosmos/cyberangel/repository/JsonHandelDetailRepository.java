package com.cosmos.cyberangel.repository;

import com.cosmos.cyberangel.entity.JsonHandelDetail;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * JsonHandelDetail Repository
 */
public interface JsonHandelDetailRepository extends JpaRepository<JsonHandelDetail, String> {
    JsonHandelDetail getJsonHandelDetailByHandelMethod(String handelMethod);
}
