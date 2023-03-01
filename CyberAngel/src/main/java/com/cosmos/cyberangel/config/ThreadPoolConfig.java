package com.cosmos.cyberangel.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.task.TaskExecutor;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import java.util.concurrent.ThreadPoolExecutor;

/**
 * ThreadPoolConfig
 */
@Configuration
public class ThreadPoolConfig {
    @Bean("requestTaskExecutor")
    public TaskExecutor requestTaskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        // Set the number of core threads
        executor.setCorePoolSize(4);
        // Set the maximum number of threads
        executor.setMaxPoolSize(8);
        // Set queue capacity
        executor.setQueueCapacity(10000);
        // Set thread name prefix
        executor.setThreadNamePrefix("RequestThread-");
        // Set rejection policy
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        // initialize
        executor.initialize();
        return executor;
    }

    @Bean("processTaskExecutor")
    public TaskExecutor processTaskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        // Set the number of core threads
        executor.setCorePoolSize(4);
        // Set the maximum number of threads
        executor.setMaxPoolSize(8);
        // Set queue capacity
        executor.setQueueCapacity(10000);
        // Set thread name prefix
        executor.setThreadNamePrefix("ProcessThread-");
        // Set rejection policy
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        // initialize
        executor.initialize();
        return executor;
    }
}
