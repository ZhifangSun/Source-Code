#!/usr/bin/env python3
# *-* coding:utf8 *-*

"""
类别: 调度器组件
名称: 调度器基类
作者: strong
邮件: jqjiang@hnist.edu.cn
日期: 2020年3月21日
说明: 所有具体调度器的基类
"""

from COMPONENT.schedulinglist import SchedulingList


class Scheduler(object):

    def __init__(self, scheduler_name):
        self.scheduler_name = scheduler_name  # 调度器名称
        self.task_scheduling_list = SchedulingList("TaskSchedulingList")  # 任务调度列表
        self.canfd_scheduling_list = SchedulingList("CanSchedulingList")  # 消息调度列表
        self.scheduling_lists = {}

    def reset(self):
        self.task_scheduling_list.list.clear()
        self.canfd_scheduling_list.list.clear()

        self.task_scheduling_list.messages.clear()
        self.canfd_scheduling_list.messages.clear()

        self.task_scheduling_list.makespan = 0.0
        self.canfd_scheduling_list.makespan = 0.0

        self.task_scheduling_lists.clear()
        self.canfd_scheduling_lists.clear()
