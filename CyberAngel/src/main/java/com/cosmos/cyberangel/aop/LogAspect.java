package com.cosmos.cyberangel.aop;

import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.Signature;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.aspectj.lang.reflect.MethodSignature;
import org.springframework.stereotype.Component;

/**
 * Auto print log aspect
 */
@Slf4j
@Aspect
@Component
public class LogAspect {

    @Pointcut("@annotation(com.cosmos.cyberangel.aop.AutoLog)")
    public void autoLog() {
    }

    @Around("autoLog()")
    public Object around(ProceedingJoinPoint joinPoint) throws Throwable {
        Signature signature = joinPoint.getSignature();
        MethodSignature methodSignature = (MethodSignature) signature;
        String className = joinPoint.getTarget().getClass().getSimpleName();
        String methodName = methodSignature.getMethod().getName();
        Object[] args = joinPoint.getArgs();
        // Print input
        log.info("Class:[{}],Method:[{}],Args:{}", className, methodName, args);
        long startTime = System.currentTimeMillis();
        Object result = joinPoint.proceed();
        long endTime = System.currentTimeMillis();
        // Print return
        log.info("Class:[{}],Method:[{}],ProcessTime:[{}ms],Result:[{}]", className, methodName, result, (endTime - startTime));
        return result;
    }
}

