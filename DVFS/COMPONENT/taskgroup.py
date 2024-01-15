#!/usr/bin/env python3
# *-* coding:utf8 *-*

"""
类别: 基本组件
名称: 任务分组类
作者: strong
邮件: jqjiang@hnist.edu.cn
日期: 2020年3月25日
说明:
"""


class TaskGroup(object):

    def __init__(self, group_id=0):
        self.group_id = group_id
        self.tasks = []

    def __str__(self):
        return "Group [group_id = %d, tasks = %s]" % (self.group_id, self.tasks)
