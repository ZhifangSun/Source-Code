#!/usr/bin/env python3
# *-* coding:utf8 *-*

"""
类别: 基本组件
名称: 消息分组类
作者: strong
邮件: jqjiang@hnist.edu.cn
日期: 2020年8月28日
说明:
"""


class MessageGroup(object):

    def __init__(self, group_id=0):
        self.group_id = group_id
        self.messages = []

    def __str__(self):
        return "Group [group_id = %d, messages = %s]" % (self.group_id, self.messages)
