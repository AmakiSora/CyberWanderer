package com.cosmos.cyberangel.job;

import com.cosmos.cyberangel.service.ParseService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

/**
 * ParseJob
 */
@Slf4j
@Component
public class ParseJob implements CommandLineRunner {

    @Autowired
    private ParseService parseService;

    @Override
    public void run(String... args) {
        log.info("ParseJob is running!");
        try {
            parseService.getParseList();
        } catch (Exception e) {
            log.error("Something's wrong with ParseJob", e);
        }
    }
}
