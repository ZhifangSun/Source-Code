#!/usr/bin/env python3
# *-* coding:utf8 *-*

"""
类别: 基本组件
名称: 任务类
作者: strong
邮件: jqjiang@hnist.edu.cn
日期: 2020年3月20日
说明: 重要的组件类
"""


class Task(object):

    def __init__(self, tid=0, name=None):
        self.id = tid   # 任务ID
        self.name = name  # 任务名称
        self.application = None  # 任务所属应用
        self.is_entry = False  # 是否为入口任务
        self.is_exit = False  # 是否为出口任务
        self.is_critical = False  # 是否为关键任务
        self.is_pseudo = False  # 是否为伪任务
        self.is_executed = False  # 是否已经运行
        self.is_ready = False     # 是否已经准备好运行
        self.isVirtual = False
        self.processor__computation_time = {}  # 处理器-执行时间值 映射
        self.processor__computation_cost = {}  # 处理器-执行成本值 映射
        self.processor__tradeoff = {}           # 处理器-任务执行时间与执行成本折衷值 映射
        self.processor__rank_up_value = {}  # 处理器-向上排序值 映射
        self.successor__communication_time = {}  # 直接后继任务-通信时间 映射
        self.successor__message = {}    # 直接后继任务-消息 映射
        self.predecessor__communication_time = {}  # 直接前驱任务-通信时间 映射
        self.predecessor__message = {}  # 直接前驱任务-消息 映射
        self.successors = []  # 任务的直接后继任务集
        self.predecessors = []  # 任务的直接前驱任务集
        self.all_successors = []    # 任务的所有后继任务集,包括直接后继任务和间接后继任务
        self.all_predecessors = []  # 任务的所有前驱任务集,包括直接前驱任务和间接前驱任务
        self.in_degree = 0  # 任务入度
        self.out_degree = 0  # 任务出度
        self.average_computation_time = 0.0  # 任务平均执行时间
        self.average_computation_cost = 0.0  # 任务平均执行成本
        self.rank_up_value = 0.0  # 任务向上排序值
        self.rank_down_value = 0.0  # 任务向下排序值
        self.rank_sum_value = 0.0  # 任务向上向下排序值之和
        self.assignment = None  # 任务运行时环境
        self.processor_CompCostMap= {}
        self.succTask_CommCostMap={}
        self.avgW=0.0
        self.outd=0
        self.makespan_st=0.0
        self.makespan_ft=0.0
        self.makespan=0.0

        self.processor = None   # 任务的执行节点
        self.execution_time = 0.0   # 任务的执行时间
        self.out_messages = []  # 任务的发送消息集
        self.in_messages = []   # 任务的接收消息集

        self.is_key = False
        self.dominate = None
        self.dominated_by = None

        self.is_transformed = False     # 任务是否已被转换成化身任务
        self.avatar = None  # 任务被转换后的化身任务

        self.is_decoded = False
        self.is_assigned = False

    def __str__(self):
        # return self.name
        return "Task [name = %s, isCritical = %s]" % (self.name, self.is_critical)

    def setProcessor_CompCostMap(self,processor_CompCostMap):
        self.processor_CompCostMap=processor_CompCostMap

    def setSuccTask_CommCostMap(self,succTask_CommCostMap):
        self.succTask_CommCostMap=succTask_CommCostMap

    def setAvgW(self,avgW):
        self.avgW=avgW

    def getSuccTask_CommCostMap(self):
        return self.succTask_CommCostMap

    def setOutd(self,outd):
        self.outd=outd

    def getOutd(self):
        return self.outd