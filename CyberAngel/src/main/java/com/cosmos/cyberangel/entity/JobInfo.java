package com.cosmos.cyberangel.entity;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Data;
import org.quartz.JobDataMap;

/**
 * JobInfo
 */
@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class JobInfo {

    private String jobClassName;

    private String jobName;

    private String jobGroupName;

    private String triggerName;

    private String triggerGroupName;

    private String cronExpression;

    private String jobDescription;

    private String triggerDescription;

    private JobDataMap jobDataMap;
}
