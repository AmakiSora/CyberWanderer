package com.cosmos.cyberangel.job;

import com.cosmos.cyberangel.entity.RequestLog;
import com.cosmos.cyberangel.repository.RequestLogRepository;
import com.cosmos.cyberangel.utils.OkHttpUtils;
import lombok.extern.slf4j.Slf4j;
import okhttp3.Response;
import org.jetbrains.annotations.NotNull;
import org.quartz.JobDataMap;
import org.quartz.JobExecutionContext;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.quartz.QuartzJobBean;
import org.springframework.stereotype.Component;

import java.io.IOException;

/**
 * RequestJob
 */
@Slf4j
@Component
public class RequestJob extends QuartzJobBean {

    @Autowired
    private RequestLogRepository requestLogRepository;

    @Override
    protected void executeInternal(@NotNull JobExecutionContext context) {
        try {
            JobDataMap jobDataMap = context.getMergedJobDataMap();
            RequestLog requestLog = RequestLog.getLogFromJobDataMap(jobDataMap);
            String url = requestLog.getRequestUrl();
            switch (requestLog.getRequestMethod().toUpperCase()) {
                case "GET" -> {
                    Response response = OkHttpUtils.get(url);
                    RequestLog save = save(requestLog, response);
                    log.debug(save.show());
                }
                case "POST" -> {
                    Response response = OkHttpUtils.post(url, requestLog.getRequestBody());
                    RequestLog save = save(requestLog, response);
                    log.debug(save.show());
                }
                case "PUT" -> {
                    Response response = OkHttpUtils.put(url, requestLog.getRequestBody());
                    RequestLog save = save(requestLog, response);
                    log.debug(save.show());
                }
                default -> {
                    String jobName = context.getJobDetail().getKey().getName();
                    log.warn("<RequestJob> JobName:[{}] error request method: [{}]", jobName, requestLog.getRequestMethod());
                }
            }
        } catch (Exception e) {
            log.error("<RequestJob> Error!",e);
        }
    }

    private RequestLog save(RequestLog requestLog, Response response) throws IOException {
        requestLog.setResponseCode(response.code());
        requestLog.setResponseHeaders(response.headers().toString());
        if (response.body() != null) {
            requestLog.setResponseBody(response.body().string());
        }
        return requestLogRepository.save(requestLog);
    }
}
