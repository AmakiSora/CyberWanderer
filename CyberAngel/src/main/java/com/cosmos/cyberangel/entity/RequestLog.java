package com.cosmos.cyberangel.entity;

import com.cosmos.cyberangel.utils.OkHttpUtils;
import jakarta.persistence.*;
import lombok.Data;
import org.quartz.JobDataMap;

import java.util.Date;

/**
 * request_response_log
 */
@Data
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

    @Column(name = "handel_method")
    private String handelMethod;

    /**
     * status
     * 0:Pending
     * 1:Processed
     * 2:Skipped
     */
    @Column(name = "status")
    private Integer status;

    public enum Status {
        PENDING,
        PROCESSED,
        SKIPPED
    }

    public String show() {
        return "RequestLog{" +
                "id=" + id + '\'' +
                ", requestUrl='" + requestUrl + '\'' +
                ", requestMethod='" + requestMethod + '\'' +
                ", requestHeaders='" + requestHeaders + '\'' +
                ", requestBody='" + requestBody + '\'' +
                ", responseCode=" + responseCode + '\'' +
                ", responseHeaders='" + responseHeaders + '\'' +
                ", responseBody='" + "ignore!" + '\'' +
                ", requestTime=" + requestTime + '\'' +
                ", status=" + status +
                '}';
    }

    public static RequestLog getLogFromJobDataMap(JobDataMap map) {
        RequestLog requestLog = new RequestLog();
        requestLog.setRequestUrl(OkHttpUtils.checkUrl(map.getString("requestUrl")));
        requestLog.setRequestHeaders(map.getString("requestHeaders"));
        requestLog.setRequestMethod(map.getString("requestMethod"));
        requestLog.setRequestBody(map.getString("requestBody"));
        int status = map.get("status") == null ? 0 : Integer.parseInt(map.get("status").toString());
        requestLog.setStatus(status);
        requestLog.setRequestTime(new Date());
        return requestLog;
    }
}
