package com.cosmos.cyberangel.controller;

import com.cosmos.cyberangel.aop.AutoLog;
import com.cosmos.cyberangel.job.Job1;
import lombok.extern.slf4j.Slf4j;
import org.quartz.*;
import org.quartz.impl.matchers.GroupMatcher;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.scheduling.quartz.SchedulerFactoryBean;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

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
     * 添加定时任务
     *
     * @param jobName          任务名称
     * @param jobGroupName     任务组名称
     * @param triggerName      触发器名称
     * @param triggerGroupName 触发器组名称
     * @param cronExpression   cron表达式
     * @return
     * @throws SchedulerException
     */
    @AutoLog
    @PostMapping("/addJob")
    public ResponseEntity<String> addJob(@RequestParam String jobName, @RequestParam String jobGroupName,
                                         @RequestParam String triggerName, @RequestParam String triggerGroupName,
                                         @RequestParam String cronExpression) throws SchedulerException {
        Scheduler scheduler = schedulerFactoryBean.getScheduler();
        JobDetail jobDetail = JobBuilder.newJob(Job1.class).withIdentity(jobName, jobGroupName).build();
        CronScheduleBuilder scheduleBuilder = CronScheduleBuilder.cronSchedule(cronExpression);
        Trigger trigger = TriggerBuilder
                .newTrigger()
                .withIdentity(triggerName, triggerGroupName)
                .withSchedule(scheduleBuilder).build();
        scheduler.scheduleJob(jobDetail, trigger);
        return ResponseEntity.ok("定时任务添加成功");
    }

    /**
     * 删除定时任务
     *
     * @param jobName          任务名称
     * @param jobGroupName     任务组名称
     * @param triggerName      触发器名称
     * @param triggerGroupName 触发器组名称
     * @return
     * @throws SchedulerException
     */
    @AutoLog
    @DeleteMapping("/deleteJob")
    public ResponseEntity<String> deleteJob(@RequestParam String jobName, @RequestParam String jobGroupName,
                                            @RequestParam String triggerName, @RequestParam String triggerGroupName) throws SchedulerException {
        Scheduler scheduler = schedulerFactoryBean.getScheduler();
        JobKey jobKey = JobKey.jobKey(jobName, jobGroupName);
        TriggerKey triggerKey = TriggerKey.triggerKey(triggerName, triggerGroupName);
        scheduler.pauseTrigger(triggerKey);
        scheduler.unscheduleJob(triggerKey);
        scheduler.deleteJob(jobKey);
        return ResponseEntity.ok("定时任务删除成功");
    }

    /**
     * 修改定时任务
     *
     * @param jobName          任务名称
     * @param jobGroupName     任务组名称
     * @param triggerName      触发器名称
     * @param triggerGroupName 触发器组名称
     * @param cronExpression   cron表达式
     * @return
     * @throws SchedulerException
     */
    @AutoLog
    @PutMapping("/updateJob")
    public ResponseEntity<String> updateJob(@RequestParam String jobName, @RequestParam String jobGroupName,
                                            @RequestParam String triggerName, @RequestParam String triggerGroupName,
                                            @RequestParam String cronExpression) throws SchedulerException {
        Scheduler scheduler = schedulerFactoryBean.getScheduler();
        TriggerKey triggerKey = TriggerKey.triggerKey(triggerName, triggerGroupName);
        CronScheduleBuilder scheduleBuilder = CronScheduleBuilder.cronSchedule(cronExpression);
        CronTrigger trigger = (CronTrigger) scheduler.getTrigger(triggerKey);
        trigger = trigger.getTriggerBuilder().withIdentity(triggerKey).withSchedule(scheduleBuilder).build();
        scheduler.rescheduleJob(triggerKey, trigger);
        return ResponseEntity.ok("定时任务修改成功");
    }

    @AutoLog
    @GetMapping("/jobs")
    public List<Map<String, Object>> listJobs() throws SchedulerException {
        List<Map<String, Object>> jobs = new ArrayList<>();
        Scheduler scheduler = schedulerFactoryBean.getScheduler();
        for (String groupName : scheduler.getJobGroupNames()) {
            for (JobKey jobKey : scheduler.getJobKeys(GroupMatcher.jobGroupEquals(groupName))) {
                JobDetail jobDetail = scheduler.getJobDetail(jobKey);
                List<Trigger> triggers = (List<Trigger>) scheduler.getTriggersOfJob(jobKey);
                Map<String, Object> job = new HashMap<>();
                job.put("name", jobKey.getName());
                job.put("group", jobKey.getGroup());
                job.put("description", jobDetail.getDescription());
                job.put("jobClass", jobDetail.getJobClass().getSimpleName());
                job.put("triggerCount", triggers.size());
                jobs.add(job);
            }
        }
        return jobs;
    }

    @AutoLog
    @GetMapping("/triggers")
    public String getTriggers() throws SchedulerException {
        List<Trigger> triggers = new ArrayList<>();
        for (String groupName : schedulerFactoryBean.getScheduler().getTriggerGroupNames()) {
            for (TriggerKey triggerKey : schedulerFactoryBean.getScheduler().getTriggerKeys(GroupMatcher.triggerGroupEquals(groupName))) {
                triggers.add(schedulerFactoryBean.getScheduler().getTrigger(triggerKey));
            }
        }
        return triggers.toString();
    }
}
