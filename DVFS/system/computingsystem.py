#!/usr/bin/env python3
# *-* coding:utf8 *-*

"""
类别: 系统组件
名称: 计算系统类
作者: strong
邮件: jqjiang@hnist.edu.cn
日期: 2020年3月20日
说明: 单例模式, 计算系统
"""

from COMPONENT import *
from COMPONENT.VRF import VRF

class ComputingSystem(object):
    instance = None  # 用于返回单例
    printOriginalSchedulingList = False
    printOptimizedSchedulingList = False
    init_flag = False  # 初始化标记

    processors = []  # 处理器集, 类属性

    applications = []  # 应用集, 类属性

    VRFs=[]
    processors1=[]
    # 私有方法, 用于向内存申请空间
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:  # 如果实例尚未生成, 则:
            cls.instance = super().__new__(cls)  # 生成它
        return cls.instance  # 并将其返回

    # 构造函数, 初始化本类
    def __init__(self, processors=None, applications=None):
        if ComputingSystem.init_flag:  # 如果初始化标志为真, 则:
            return  # 直接中断. 表示只初始化一遍, 如此可以确保内存中只有一个计算系统类存在
        self.processors = processors  #
        self.applications = applications  #
        ComputingSystem.init_flag = True  # 置初始化标志为真

    # 初始化计算系统, 类方法
    @classmethod
    def init(cls, processor_number):
        ComputingSystem.init_processors(processor_number)  # 初始化处理器集

    # 初始化处理器集, 类方法
    @classmethod
    def init_processors(cls, processor_number):
        for i in range(processor_number):  # 遍历处理器数
            ecu = processor.Processor((i + 1), "P%d" % (i + 1))      # 命名处理器, 循环变量+1
            cls.processors.append(ecu)  # 向处理器集中添加命名后的处理器

    # 清洗处理器 —— 清空驻留任务集, 类方法
    @classmethod
    def clear_processors(cls):
        for p in cls.processors:
            p.resident_tasks.clear()

    # 清空应用
    @classmethod
    def clear_applications(cls):
        cls.applications.clear()

    # 重置处理器
    @classmethod
    def reset_processors(cls):
        cls.clear_processors()

    # 重置任务
    @classmethod
    def reset_tasks(cls, app):
        for t in app.tasks:
            t.is_executed = False
            t.is_assigned = False
            t.assignment = None

    # 计算系统重置
    @classmethod
    def reset(cls, app):
        cls.reset_processors()
        cls.reset_tasks(app)

    @classmethod
    def initiateVRFs(cls,vrfs):
        for i in range(len(vrfs)):
            Vrf=[]
            vrf=vrfs[i]
            for j in range(len(vrf)):
                v=VRF(vrf[j][0],vrf[j][1])
                Vrf.append(v)
            cls.VRFs.append(Vrf)

    @classmethod
    def initiateProcessors(cls,vrfs,processorNumber):
        for i in range(processorNumber):
            p = processor.Processor((i+1), "p%d" % (i+1))
            p.setVrfs(cls.VRFs[i%len(cls.VRFs)])
            cls.processors.append(p)

    @classmethod
    def initiate(cls,vrfs,processorNumber):
        cls.initiateVRFs(vrfs)
        cls.initiateProcessors(vrfs, processorNumber)