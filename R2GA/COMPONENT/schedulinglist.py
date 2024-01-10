#!/usr/bin/env python3
# *-* coding:utf8 *-*

"""
类别: 调度器组件
名称: 调度列表类
作者: strong
邮件: jqjiang@hnist.edu.cn
日期: 2020年3月21日
说明: 保存任务与对应运行时环境的组件类
"""


class SchedulingList(object):

    def __init__(self, list_name=None, list_id=0):
        self.list_name = list_name  # 列表名称
        self.list_id = list_id  # 列表ID
        self.list = {}  # 字典类型, 用于保留任务与其对应运行时环境
        self.msg_list = {}
        self.messages = []
        self.makespan = 0.0  # 列表完工时间
        self.cost = 0.0     # 列表执行成本
        self.allE = 0.0

    def __str__(self):
        return "SchedulingList [list_name = %s, list = %s]" % (self.list_id, self.list)
