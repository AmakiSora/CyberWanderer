package com.cosmos.cyberangel.controller;

import com.cosmos.cyberangel.aop.AutoLog;
import com.cosmos.cyberangel.entity.JobInfo;
import com.cosmos.cyberangel.entity.ResponseVO;
import lombok.extern.slf4j.Slf4j;
import org.quartz.*;
import org.quartz.impl.matchers.GroupMatcher;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.quartz.QuartzJobBean;
import org.springframework.scheduling.quartz.SchedulerFactoryBean;
import org.springframework.util.ObjectUtils;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;

/**
 * Scheduled Tasks Controller
 */
@Slf4j
@RestController
@RequestMapping("/task")
public class TaskController {
    @Autowired
    private SchedulerFactoryBean schedulerFactoryBean;

    /**
     * addJob
     */
    @AutoLog
    @PostMapping("/addJob")
    public ResponseVO<?> addJob(@RequestBody JobInfo jobInfo) {
        try {
            Scheduler scheduler = schedulerFactoryBean.getScheduler();
            String className = "com.cosmos.cyberangel.job." + jobInfo.getJobClassName();
            Class<? extends QuartzJobBean> jobClass = (Class<? extends QuartzJobBean>) Class.forName(className);
            JobDetail jobDetail = JobBuilder
                    .newJob(jobClass)
                    .withIdentity(jobInfo.getJobName(), jobInfo.getJobGroupName())
                    .withDescription(jobInfo.getJobDescription())
                    .setJobData(jobInfo.getJobDataMap())
                    .build();
            Trigger trigger = TriggerBuilder
                    .newTrigger()
                    .withIdentity(jobInfo.getTriggerName(), jobInfo.getTriggerGroupName())
                    .withDescription(jobInfo.getTriggerDescription())
                    .withSchedule(CronScheduleBuilder.cronSchedule(jobInfo.getCronExpression()))
                    .build();
            scheduler.scheduleJob(jobDetail, trigger);
            return ResponseVO.ok("Add job success!");
        } catch (ClassNotFoundException e) {
            log.error("Add job fail!", e);
            return ResponseVO.error("add job fail! class " + e.getMessage() + " not found!");
        } catch (Exception e) {
            log.error("Add job fail!", e);
            return ResponseVO.error("Add job fail!", e.getMessage());
        }
    }

    /**
     * deleteJob
     */
    @AutoLog
    @DeleteMapping("/deleteJob")
    public ResponseVO<?> deleteJob(@RequestParam String jobName,
                                   @RequestParam String jobGroupName) {
        try {
            Scheduler scheduler = schedulerFactoryBean.getScheduler();
            JobKey jobKey = JobKey.jobKey(jobName, jobGroupName);
            JobDetail jobDetail = scheduler.getJobDetail(jobKey);
            if (ObjectUtils.isEmpty(jobDetail)) {
                return ResponseVO.error("Delete job [" + jobName + "] fail!",
                        "Please check that the task you want to delete already exists!");
            }
            JobInfo jobInfo = new JobInfo();
            jobInfo.setJobName(jobDetail.getKey().getName());
            jobInfo.setJobGroupName(jobDetail.getKey().getGroup());
            jobInfo.setJobClassName(jobDetail.getJobClass().getSimpleName());
            jobInfo.setJobDescription(jobDetail.getDescription());
            if (scheduler.deleteJob(jobKey)) {
                return ResponseVO.ok("Delete job [" + jobName + "] success!", jobInfo);
            } else {
                return ResponseVO.error("Delete job [" + jobName + "] fail!");
            }
        } catch (Exception e) {
            log.error("Delete job [" + jobName + "] fail!", e);
            return ResponseVO.error("Delete job [" + jobName + "] fail!", e.getMessage());
        }
    }

    /**
     * updateJob
     */
    @AutoLog
    @PutMapping("/updateJob")
    public ResponseVO<?> updateJob(@RequestBody JobInfo jobInfo) {
        try {
            Scheduler scheduler = schedulerFactoryBean.getScheduler();
            TriggerKey triggerKey = TriggerKey.triggerKey(jobInfo.getTriggerName(), jobInfo.getTriggerGroupName());
            CronScheduleBuilder scheduleBuilder = CronScheduleBuilder.cronSchedule(jobInfo.getCronExpression());
            CronTrigger trigger = (CronTrigger) scheduler.getTrigger(triggerKey);
            trigger = trigger
                    .getTriggerBuilder()
                    .withIdentity(triggerKey)
                    .withSchedule(scheduleBuilder)
                    .build();
            scheduler.rescheduleJob(triggerKey, trigger);
            return ResponseVO.ok("Update job success!");
        } catch (Exception e) {
            log.error("Update job fail!", e);
            return ResponseVO.error("Update job fail!", e.getMessage());
        }
    }

    /**
     * jobs
     */
    @AutoLog
    @GetMapping("/jobs")
    public ResponseVO<?> jobs() throws SchedulerException {
        List<JobInfo> jobs = new ArrayList<>();
        Scheduler scheduler = schedulerFactoryBean.getScheduler();
        for (String groupName : scheduler.getJobGroupNames()) {
            for (JobKey jobKey : scheduler.getJobKeys(GroupMatcher.jobGroupEquals(groupName))) {
                JobDetail jobDetail = scheduler.getJobDetail(jobKey);
                JobInfo jobInfo = new JobInfo();
                jobInfo.setJobName(jobKey.getName());
                jobInfo.setJobGroupName(jobKey.getGroup());
                jobInfo.setJobClassName(jobDetail.getJobClass().getSimpleName());
                jobInfo.setJobDescription(jobDetail.getDescription());
                jobs.add(jobInfo);
            }
        }
        return ResponseVO.ok("", jobs);
    }

    /**
     * triggers
     */
    @AutoLog
    @GetMapping("/triggers")
    public ResponseVO<?> getTriggers() throws SchedulerException {
        List<Trigger> triggers = new ArrayList<>();
        for (String groupName : schedulerFactoryBean.getScheduler().getTriggerGroupNames()) {
            for (TriggerKey triggerKey : schedulerFactoryBean.getScheduler().getTriggerKeys(GroupMatcher.triggerGroupEquals(groupName))) {
                triggers.add(schedulerFactoryBean.getScheduler().getTrigger(triggerKey));
            }
        }
        return ResponseVO.ok("", triggers.toString());
    }
}
