package com.cosmos.cyberangel.controller;

import com.cosmos.cyberangel.aop.AutoLog;
import com.cosmos.cyberangel.entity.ResponseVO;
import com.cosmos.cyberangel.service.RequestService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.MissingServletRequestParameterException;
import org.springframework.web.bind.annotation.*;

/**
 * Request Controller
 */
@Slf4j
@RestController
@RequestMapping("/request")
public class RequestController {

    @Autowired
    private RequestService requestService;

    @ExceptionHandler(MissingServletRequestParameterException.class)
    public ResponseVO<?> handleMissingServletRequestParameterException(MissingServletRequestParameterException e) {
        return ResponseVO.error("Missing parameter：" + e.getParameterName());
    }

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
