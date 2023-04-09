package com.cosmos.cyberangel.entity;

import jakarta.persistence.*;
import lombok.Data;

/**
 * json_handel_detail
 */
@Data
@Entity
@Table(name = "json_handel_detail")
public class JsonHandelDetail {
    @Id
    @Column(name = "handel_method")
    private String handelMethod;

    @Column(name = "handel_detail")
    private String handelDetail;
}
