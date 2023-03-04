package com.cosmos.cyberangel.config;

import com.cosmos.cyberangel.entity.ResponseVO;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.MissingServletRequestParameterException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

/**
 * GlobalExceptionHandler
 */
@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(MissingServletRequestParameterException.class)
    public ResponseVO<?> handleMissingServletRequestParameterException(MissingServletRequestParameterException e) {
        return ResponseVO.error("Missing parameter：" + e.getParameterName());
    }

    @ExceptionHandler(Exception.class)
    public ResponseVO<?> handleAllException(Exception e) {
        log.error("Service error!", e);
        return ResponseVO.error(e.getMessage());
    }
}