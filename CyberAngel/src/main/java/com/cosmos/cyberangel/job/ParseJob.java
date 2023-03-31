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

import java.util.List;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

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

    private final Set<Long> processingSet = ConcurrentHashMap.newKeySet();

    @Override
    public void run(String... args) {
        log.info("<ParseJob> Start!");
        try {
            while (true) {
                List<RequestLog> parseList = parseService.getParseList(RequestLog.Status.PENDING.ordinal(), processingSet);
                log.info("<ParseJob> Parse list count:[{}]", parseList.size());
                for (RequestLog requestLog : parseList) {
                    if (!processingSet.add(requestLog.getId())) {
                        log.info("<ParseJob> Processing id:[{}],already processing!", requestLog.getId());
                        continue;
                    }
                    taskExecutor.execute(() -> {
                        try {
                            log.info("<ParseJob> Processing id:[{}],task start!", requestLog.getId());
                            Thread.sleep(1000);
                        } catch (Exception e) {
                            log.error("<ParseJob> Error!", e);
                        } finally {
                            processingSet.remove(requestLog.getId());
                            log.info("<ParseJob> Processing id:[{}],task end!", requestLog.getId());
                        }
                    });
                }
                ThreadPoolTaskExecutor threadPoolTaskExecutor = (ThreadPoolTaskExecutor) taskExecutor;
                log.info("<ParseJob> Task queue count:[{}],processing set count:[{}]", threadPoolTaskExecutor.getQueueSize(), processingSet.size());
            }
        } catch (Exception e) {
            log.error("<ParseJob> Error!", e);
        }
    }
}
