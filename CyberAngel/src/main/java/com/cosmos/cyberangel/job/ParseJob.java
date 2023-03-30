package com.cosmos.cyberangel.job;

import com.cosmos.cyberangel.entity.RequestLog;
import com.cosmos.cyberangel.service.ParseService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.task.TaskExecutor;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;

/**
 * ParseJob
 */
@Slf4j
@Component
public class ParseJob implements CommandLineRunner {

    @Autowired
    private ParseService parseService;
    @Autowired
    @Qualifier("processTaskExecutor")
    private TaskExecutor taskExecutor;

    @Override
    public void run(String... args) {
        log.info("<ParseJob> Start!");
        try {
            while (true) {
                List<RequestLog> parseList = parseService.getParseList(RequestLog.Status.PENDING.ordinal(), new ArrayList<>());
                log.info("<ParseJob> parseList->{}", parseList);
                for (RequestLog requestLog : parseList) {
                    taskExecutor.execute(() -> {
                        log.info("<ParseJob> requestLog->{}", requestLog);
                    });
                }
                ThreadPoolTaskExecutor threadPoolTaskExecutor = (ThreadPoolTaskExecutor) taskExecutor;
                log.info("<ParseJob> QueueSize->{}", threadPoolTaskExecutor.getQueueSize());
            }
        } catch (Exception e) {
            log.error("<ParseJob> Error!", e);
        }
    }
}
