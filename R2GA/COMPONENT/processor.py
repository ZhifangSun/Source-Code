#!/usr/bin/env python3
# *-* coding:utf8 *-*

"""
类别: 基本组件
名称: 处理器类
作者: strong
邮件: jqjiang@hnist.edu.cn
日期: 2020年3月20日
说明: 驻留任务集是被分配到处理器上的所有任务的集合
"""

from COMPONENT.VRF import VRF

class Processor(object):

    def __init__(self, pid=0, name=None):
        self.id = pid
        self.name = name  # 处理器名称
        self.resident_tasks = []  # 处理器驻留任务集
        self.vrfs=[]
        self.getTask_AvailTimeMap= {}
        self.getTask_RunningTimeMap={}

    def __str__(self):
        return "Processor [id = %d, name = %s]" % (self.id, self.name)

    def setVrfs(self,vrfs):
        self.vrfs.append(vrfs)

    def getVrfs(self):
        return self.vrfs