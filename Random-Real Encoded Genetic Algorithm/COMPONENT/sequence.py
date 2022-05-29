#!/usr/bin/env python3
# *-* coding:utf8 *-*

"""
类别: 调度器组件
名称: 调度列表类
作者: strong
邮件: jqjiang@hnist.edu.cn
日期: 2020年9月20日
说明: 随机数序列类
"""

from CONFIG.config import *


class Sequence(object):

    def __init__(self, chromosome=None, tsk_sequence=None, prossor_sequence=None, makespan=0.0, cost=0.0):
        self.temp_list=None
        self.chromosome = chromosome
        self.index_population=None
        self.index_list=None
        self.tsk_sequence = tsk_sequence
        self.prossor_sequence = prossor_sequence
        self.makespan = makespan
        self.cost = cost
        self.tradeoff = ALPHA * makespan + BETA * cost
        self.scheduling_list=None
        self.lf=None
        self.ft=None

