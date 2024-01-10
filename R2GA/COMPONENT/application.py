#!/usr/bin/env python3
# *-* coding:utf8 *-*

"""
类别: 基本组件
名称: 应用类
作者: strong
邮件: jqjiang@hnist.edu.cn
日期: 2020年3月21日
说明: 
"""


class Application(object):

    def __init__(self, name=None):
        self.tasknum=None
        self.processor_number=None
        self.name = name  # 应用名称
        self.OR=None
        self.ORnum=0
        self.ctm=None
        self.OR_in=None
        self.not_in_OR=None
        self.computation_time_matrix=None
        self.criticality = 0  # 应用重要/紧急程度
        self.entry_task = []  # 应用入口任务
        self.exit_task = []  # 应用出口任务
        self.IPPS_entry_task=[]
        self.IPPS_exit_task = []
        self.tasks = []  # 应用任务集
        self.authenticated_tasks = []
        self.prioritized_tasks = []  # 排序后任务集
        self.critical_tasks = []  # 应用关键任务集
        self.deadline = 0.0  # 应用截止时间
        self.budget = 0.0  # 应用可用成本
        self.task_groups_from_the_top = {}
        self.task_groups_from_the_bottom = {}

        self.all_messages = []  # 应用的消息集
        self.valid_messages = []    # 应用的有效消息集
        self.prioritized_messages = []  # 排序后消息集
        self.temp_messages = []     # 用于转换时存放半成品消息
        self.message_groups_from_the_top = {}

        self.sequences = []
        self.arrivalTime = 0.0
        self.communicationMatrix = None
        self.deadline = 0.0
        self.originalDeadline = 0.0
        self.cp_min_time = 0.0  # 关键路径任务最小执行时间之和
        self.cp_min_cost = 0.0  # 关键路径任务最小执行成本之和

    def __str__(self):
        return "Application [name = %s]" % self.name

    def setArrivalTime(self,arrivalTime):
        self.arrivalTime = arrivalTime

    def setCommunicationMatrix(self,communicationMatrix):
        self.communicationMatrix = communicationMatrix

    def setDeadline(self,deadline):
        self.deadline = deadline

    def setOriginalDeadline(self,originalDeadline):
        self.originalDeadline = originalDeadline