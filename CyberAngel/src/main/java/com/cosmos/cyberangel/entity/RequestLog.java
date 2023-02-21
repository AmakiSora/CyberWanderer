package com.cosmos.cyberangel.entity;

import jakarta.persistence.*;

import java.util.Date;

/**
 * request_response_log
 */
@Entity
@Table(name = "request_response_log")
public class RequestLog {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "request_url")
    private String requestUrl;

    @Column(name = "request_method")
    private String requestMethod;

    @Column(name = "request_headers")
    private String requestHeaders;

    @Column(name = "request_body")
    private String requestBody;

    @Column(name = "response_code")
    private Integer responseCode;

    @Column(name = "response_headers")
    private String responseHeaders;

    @Column(name = "response_body")
    private String responseBody;

    @Column(name = "request_time")
    private Date requestTime;

    @Column(name = "status")
    private Integer status;
}
