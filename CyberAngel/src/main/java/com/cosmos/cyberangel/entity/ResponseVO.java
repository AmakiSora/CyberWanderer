package com.cosmos.cyberangel.entity;

import lombok.Data;

/**
 * ResponseVO
 */
@Data
public class ResponseVO<T> {
    private int code;
    private String message;
    private T data;

    private ResponseVO(int code, String message, T data) {
        this.code = code;
        this.message = message;
        this.data = data;
    }

    public static <T> ResponseVO<T> ok() {
        return ResponseVO.ok(null);
    }

    public static <T> ResponseVO<T> ok(String message) {
        return ResponseVO.ok(message, null);
    }

    public static <T> ResponseVO<T> ok(String message, T data) {
        return new ResponseVO<>(200, message, data);
    }

    public static <T> ResponseVO<T> error() {
        return ResponseVO.error(null);
    }

    public static <T> ResponseVO<T> error(String message) {
        return ResponseVO.error(message, null);
    }

    public static <T> ResponseVO<T> error(String message, T data) {
        return new ResponseVO<>(500, message, data);
    }

}
