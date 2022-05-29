#!/usr/bin/env python3
# *-* coding:utf8 *-*

"""
类别: 基本组件
名称: 运行时间段类
作者: strong
邮件: jqjiang@hnist.edu.cn
日期: 2020年3月20日
说明: 包括启动时间, 结束时间以及二者之间的时间跨度
"""


class RunningSpan(object):

    def __init__(self, start_time=0, finish_time=0):
        self.start_time = start_time  # 运行启动时间
        self.finish_time = finish_time  # 运行结束时间
        self.span = self.finish_time - self.start_time  # 运行持续时间

    def __str__(self):
        # return "RunningSpan [start_time = %.2f, finish_time = %.2f, span = %.2f]" % (self.start_time, self.finish_time, self.span)
        return "[%.2f, %.2f]" % (self.start_time, self.finish_time)

