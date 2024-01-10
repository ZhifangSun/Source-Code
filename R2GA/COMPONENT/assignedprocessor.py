#!/usr/bin/env python3
# *-* coding:utf8 *-*

"""
类别: 基本组件
名称: 运行时环境分配类
作者: szf
邮件: zf_sun@vip.hnist.edu.cn
日期: 2022年3月1日
说明: 保存任务运行时的所分配处理器、运行时间段、电压和频率组等信息的组件类
"""


class AssignedProcessor(object):

    def __init__(self, assigned_processor=None, vrf=None,running_span=None):
        self.assigned_processor = assigned_processor  # 任务所分配处理器
        self.vrf=vrf
        self.running_span = running_span  # 任务运行时间段

    def __str__(self):
        return "Assignment [assigned_processor = %s, vrf = %s, running_span = %s]" % (self.assigned_processor, self.vrf, self.running_span)
