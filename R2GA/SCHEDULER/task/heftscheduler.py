#!/usr/bin/env python3
# *-* coding:utf8 *-*

"""
类别: 调度器
名称: HEFT调度器
作者: strong
邮件: jqjiang@hnist.edu.cn
日期: 2020年3月21日
说明: 来源Paper: Performance-effective and low-complexity task scheduling for heterogeneous computing
"""

from COMPONENT.runningspan import RunningSpan
from COMPONENT.assignment import Assignment
from SCHEDULER.scheduler import Scheduler
from system.computingsystem import ComputingSystem
from UTIL.schedulerutils import SchedulerUtils
from UTIL.genericutils import *
from CONFIG.config import *


class HeftScheduler(Scheduler):
    '''
    # 基类 Scheduler 中已经实现了构造方法 __init__ , 因此本类中的构造方法 __init__ 可以省略
    def __init__(self, scheduler_name):
        super(scheduler_name)
        self.scheduler_name = scheduler_name
        self.original_scheduling_list = SchedulingList("OriginalSchedulingList")
    '''

    # 具体调度方法
    def schedule(self, app):

        ComputingSystem.reset(app)  # 重置计算系统. !!!VERY IMPORTANT!!!

        processors = ComputingSystem.processors  # 处理器集

        tasks = app.prioritized_tasks  # 排序任务集
        tasks.sort(key=lambda tsk: tsk.rank_up_value, reverse=True)

        processor = None  # 全局处理器
        temp_task_id=[]
        temp_processor_id = []

        for task in tasks:  # 遍历排序任务集

            earliest_start_time = 0.0  # 初始化全局最早启动时间为0
            earliest_finish_time = float("inf")  # 初始化全局最早结束时间为无穷大

            for p in processors:  # 遍历处理器集

                earliest_start_time_of_this_processor = SchedulerUtils.calculate_earliest_start_time(task, p)  # 当前遍历处理器上最早可用启动时间
                earliest_finish_time_of_this_processor = earliest_start_time_of_this_processor + task.processor__computation_time[p]  # 当前遍历处理器上最早可用结束时间

                if earliest_finish_time > earliest_finish_time_of_this_processor:  # 如果全局最早启动时间大于当前遍历处理器上最早可用启动时间, 则
                    earliest_start_time = earliest_start_time_of_this_processor  # 设置全局最早启动时间为当前遍历处理器上最早可用启动时间
                    earliest_finish_time = earliest_finish_time_of_this_processor  # 设置全局最早结束时间为当前遍历处理器上最早可用结束时间
                    processor = p  # 设置全局处理器为当前遍历处理器

            running_span = RunningSpan(earliest_start_time, earliest_finish_time)  # 上述 for 循环结束后, 最合适的处理器已被找出, 此时可以记录下任务的运行时间段
            assignment = Assignment(processor, running_span)  # 同时记录下任务的运行时环境

            task.assignment = assignment  # 设置任务的运行时环境

            task.is_assigned = True  # 标记任务已被分配

            processor.resident_tasks.append(task)  # 将任务添加至处理器的驻留任务集中
            temp_task_id.append(task.id)
            temp_processor_id.append(processor.id)
            processor.resident_tasks.sort(key=lambda tsk: tsk.assignment.running_span.start_time)  # 对处理器的驻留任务进行排序, 依据任务启动时间升序排列

            self.task_scheduling_list.list[task] = assignment  # 将任务与对应运行时环境置于原始调度列表

        makespan = calculate_makespan(self.task_scheduling_list)
        cost = calculate_cost(self.task_scheduling_list)
        self.task_scheduling_list.makespan = makespan
        self.task_scheduling_list.cost = cost

        print("The scheduler = %s, list_name = %s, makespan = %.2f, cost = %.2f, tradeoff = %.2f" % (self.scheduler_name,
                                                                       self.task_scheduling_list.list_name,
                                                                       makespan, cost,
                                                                       makespan * ALPHA + cost * BETA))

        # if SHOW_ORIGINAL_SCHEDULING_LIST:  # 如果打印原始调度列表, 则:
        #     print_scheduling_list(self.task_scheduling_list)  # 打印原始调度列表

        #return makespan * ALPHA + cost * BETA
        return temp_task_id.extend(temp_processor_id)
