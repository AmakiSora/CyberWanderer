package com.cosmos.cyberangel.controller;

import com.cosmos.cyberangel.aop.AutoLog;
import com.cosmos.cyberangel.entity.ResponseVO;
import com.cosmos.cyberangel.service.RequestService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * Request Controller
 */
@Slf4j
@RestController
@RequestMapping("/request")
public class RequestController {

    @Autowired
    private RequestService requestService;

    @AutoLog
    @GetMapping("/get")
    public ResponseVO<?> get(@RequestParam String url) {
        try {
            url = requestService.checkUrl(url);
            String responseBody = requestService.get(url);
            return ResponseVO.ok("Request succeeded!", responseBody);
        } catch (Exception e) {
            log.error("/request/get", e);
            return ResponseVO.error(e.getMessage());
        }
    }

    @AutoLog
    @GetMapping("/post")
    public ResponseVO<?> post(@RequestParam String url, @RequestParam String json) {
        try {
            url = requestService.checkUrl(url);
            String responseBody = requestService.post(url, json);
            return ResponseVO.ok("Request succeeded!", responseBody);
        } catch (Exception e) {
            log.error("/request/post", e);
            return ResponseVO.error(e.getMessage());
        }
    }

    @AutoLog
    @GetMapping("/put")
    public ResponseVO<?> put(@RequestParam String url, @RequestParam String json) {
        try {
            url = requestService.checkUrl(url);
            String responseBody = requestService.put(url, json);
            return ResponseVO.ok("Request succeeded!", responseBody);
        } catch (Exception e) {
            log.error("/request/put", e);
            return ResponseVO.error(e.getMessage());
        }
    }

}
