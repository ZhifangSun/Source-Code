#!/usr/bin/env python3
# *-* coding:utf8 *-*

"""
类别: 基本组件
名称: 消息类
作者: strong
邮件: jqjiang@hnist.edu.cn
日期: 2020年8月25日
说明:
"""


class Message(object):

    def __init__(self, mid=0, name=None):
        self.id = mid
        self.name = name    # 消息名称
        self.source = None  # 消息发送端
        self.target = None     # 消息接收端
        self.transmission_time = 0.0       # 消息传输时间
        self.transmission_span = None
        self.rank_up_value = 0.0   # 消息向上排序值
        self.start_transmit_time = 0.0      # 传输启动时间
        self.finish_transmit_time = 0.0     # 传输结束时间
        self.immediate_successor_messages = []  # 消息的直接前驱消息集
        self.immediate_predecessor_messages = []    # 消息的直接后继消息集
        self.all_successor_messages = []        # 消息的所有前驱消息集
        self.all_predecessor_messages = []      # 消息的所有后继消息集
        self.all_successor_messages_lite = []  # 消息的所有前驱消息名称集
        self.all_predecessor_messages_lite = []  # 消息的所有后继消息名称集
        self.is_transmitted = False
        self.is_pseudo = False

    def rename(self, new_name):
        self.name = new_name

    def __str__(self):
        return "["+self.name+"]"
        # return "Message [name = %s]" % self.name
        # return "%s\t[%.2f, %.2f]\t%.2f" % (self.name, self.start_transmit_time, self.finish_transmit_time, self.transmission_time)
        # return "Message [name = %s, transmission_time = %.2f, transmission_span=[%.2f, %.2f]]" % (self.name, self.transmission_time, self.start_transmit_time, self.finish_transmit_time)
        # return "Message [name = %s, source = %s, target = %s, trans_time = %f, rank_up_value = %f]" % (self.name, self.source, self.target, self.transmission_time, self.rank_up_value)
