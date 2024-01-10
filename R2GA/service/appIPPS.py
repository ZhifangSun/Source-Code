#!/usr/bin/env python3
# *-* coding:utf8 *-*

"""
类别: 服务组件
名称: 应用服务类
作者: strong
邮件: jqjiang@hnist.edu.cn
日期: 2020年3月21日
说明: 对应用进行初始化等操作的服务工具类
"""

from CONFIG.config import *
from COMPONENT.application import Application
from COMPONENT.task import Task
from COMPONENT.taskgroup import TaskGroup
from COMPONENT.message import Message
from COMPONENT.messagegroup import MessageGroup
from system.computingsystem import ComputingSystem
from UTIL.genericutils import print_list
from UTIL.schedulerutils import SchedulerUtils
from UTIL.genericutils import *


class ApplicationService(object):

    # 初始化应用, 静态方法
    @staticmethod
    def init_application(app, OR_in, not_in_OR, OR, ORnum, task_number, computation_time_matrix, ctm, communication_time_matrix):
        app.ORnum=ORnum
        app.ctm=ctm
        app.OR=OR
        app.OR_in=OR_in
        app.not_in_OR=not_in_OR
        ApplicationService.__init_task_list(app, task_number)                       # 初始化任务列表
        ApplicationService.__init_computation_time(app, computation_time_matrix)    # 初始化执行时间
        # ApplicationService.__init_computation_cost(app, computation_cost_matrix)  # 初始化执行时间

        ApplicationService.__init_successor(app, communication_time_matrix)         # 初始化后继任务
        ApplicationService.__init_predecessor(app)                                  # 初始化前驱任务

        ApplicationService.__init_all_successor(app)
        ApplicationService.__init_all_predecessor(app)

        # ApplicationService.__calculate_rank_up_value(app)                           # 计算任务向上排序值
        # ApplicationService.__calculate_rank_down_value(app)                         # 计算任务向下排序值
        # ApplicationService.__calculate_rank_sum_value(app)                          # 计算任务向上向下排序值之和
        # ApplicationService.__calculate_tradeoff_with_alpha_and_beta(app, ALPHA, BETA)    # 计算任务的折衷值

        ApplicationService.__tag_entry_and_exit_task(app)                           # 标记入口和出口任务
        # ApplicationService.__tag_critical_task(app)                                 # 标记关键路径任务

        # ApplicationService.__calculate_cp_min_x(app)                                # 计算关键路径任务的最小执行时间以及成本

        ApplicationService.__group_task_from_the_top(app)                           # 再次对[转换后的]任务进行分层

        ApplicationService.__init_message(app)                                      # 初始化消息的前驱、后继消息集
        ApplicationService.__group_message_from_the_top(app)                        # 对消息进行分层

        pass

    # 初始化任务列表, 静态私有方法
    @staticmethod
    def __init_task_list(app, task_number):
        for i in range(task_number):
            t = Task((i + 1), "%s-task-%d" % (app.name, (i + 1)))  # 给任务取名
            t.application = app  # 设置任务所属应用
            app.tasks.append(t)  # 将任务添加至应用任务集
            app.prioritized_tasks.append(t)  # 同时将任务添加至应用排序任务集

    # 初始化任务执行时间, 静态私有方法
    @staticmethod
    def __init_computation_time(app, computation_time_matrix):

        if not computation_time_matrix:  # 如果执行时间矩阵为空, 则:
            return  # 直接返回, 什么也不做
        app.computation_time_matrix=computation_time_matrix
        processors = ComputingSystem.processors  # 处理器集

        for i in range(len(app.tasks)):  # 遍历应用任务集
            task = app.tasks[i]  # 取当前遍历任务
            s = 0.0
            for j in range(len(processors)):  # 遍历处理器集
                processor = processors[j]  # 取当前遍历处理器
                if j+1 in computation_time_matrix[i].keys():
                    computation_time = computation_time_matrix[i][j+1]
                    task.processor__computation_time[processor] = computation_time  # 设置任务的 处理器-执行时间值 为矩阵中对应值
                else:
                    computation_time = INF
                    task.processor__computation_time[processor] = computation_time
            #     s = s + computation_time
            # task.average_computation_time = s / len(processors)

    # 初始化任务的直接后继任务, 静态私有方法
    @staticmethod
    def __init_successor(app, communication_time_matrix):

        if not communication_time_matrix:  # 如果通信时间矩阵为空, 则:
            return  # 直接返回, 什么也不做

        k = 0

        for i in range(len(app.tasks)):  # 遍历任务集
            task = app.tasks[i]  # 取当前遍历任务
            communication_times = communication_time_matrix[i]  # 取当前遍历任务的通信时间行值
            for j in range(len(communication_times)):  # 遍历通信时间行值
                communication_time = communication_times[j]
                if communication_time != INF:  # 如果存在通信时间, 则:
                    successor = app.tasks[j]  # 根据 j 值获得一个直接后继任务
                    task.successor__communication_time[successor] = communication_time  # 设置任务的 后继任务-通信时间值 为矩阵中对应值
                    task.successors.append(successor)  # 将后继任务置入任务的直接后继任务集

                    k = k + 1

                    message = Message(k, "m%d,%d" % (i+1, j+1))    # VERY IMPORTANT!!! 此处的(i+1)请严格参照任务的命名方式, 要与任务的命名方式严格保持一致
                    message.source = task                       # 设定消息的发送端任务
                    message.target = successor                  # 设定消息的接收端任务
                    message.transmission_time = communication_time  # 设定消息的传输时间
                    app.all_messages.append(message)                # 将消息添加进应用的消息集
                    if message.transmission_time > 0.0:        # 判断当前消息是否为有效消息, 判断依据为: 传输时间大于0的为有效消息
                        app.valid_messages.append(message)      # 将有效消息添加进应用的有效消息集
                    else:
                        message.is_pseudo = True

                    task.successor__message[successor] = message    # 设定当前任务与直接后继任务之间的传输消息

                    task.out_messages.append(message)           # 将消息添加进当前任务的发送消息集
                    successor.in_messages.append(message)       # 将消息添加进直接后继任务的接收消息集

            task.out_degree = len(task.successors)  # 最后根据直接后继任务个数, 求得任务的出度

    # 初始化任务的直接前驱任务, 静态私有方法
    @staticmethod
    def __init_predecessor(app):
        for i in range(len(app.tasks)):  # 遍历任务集
            task = app.tasks[i]  # 取当前遍历任务
            for successor in task.successors:  # 遍历当前任务的直接后继任务集
                communication_time = task.successor__communication_time[successor]  # 取与后继任务的通信时间
                successor.predecessor__communication_time[task] = communication_time  # 设置后继任务的 前驱任务-通信时间值
                successor.predecessors.append(task)  # 将当前遍历任务添加至后继任务的直接前驱任务集中

                message = task.successor__message[successor]
                successor.predecessor__message[task] = message

            task.in_degree = len(task.predecessors)  # 最后根据直接前驱任务个数，求得任务的入度

    # 初始化任务的所有后继任务, 静态私有化方法
    @staticmethod
    def __init_all_successor(app):
        for i in range(len(app.tasks) - 1, -1, -1):  # 倒序遍历任务集, 注意: 终点值是 -1 , 不是 0
            task = app.tasks[i]  # 取当前遍历任务
            if task.is_exit:
                task.all_successors.extend([])
            else:
                successors = task.successors
                task.all_successors.extend(successors)
                for successor in successors:
                    task.all_successors.extend(successor.all_successors)
            compact_list = list(set(task.all_successors))
            compact_list.sort(key=lambda t: t.id)
            task.all_successors.clear()
            task.all_successors.extend(compact_list)

    # 初始化任务的所有前驱任务, 静态私有化方法
    @staticmethod
    def __init_all_predecessor(app):
        for i in range(len(app.tasks)):  # 遍历任务集
            task = app.tasks[i]  # 取当前遍历任务
            if task.is_entry:
                task.all_predecessors.extend([])
            else:
                predecessors = task.predecessors
                task.all_predecessors.extend(predecessors)
                for predecessor in predecessors:
                    task.all_predecessors.extend(predecessor.all_predecessors)
            compact_list = list(set(task.all_predecessors))
            compact_list.sort(key=lambda t: t.id)
            task.all_predecessors.clear()
            task.all_predecessors.extend(compact_list)

    # 初始化应用的有效消息集
    @staticmethod
    def __init_message(app):
        for message in app.all_messages:
            source = message.source
            target = message.target
            all_predecessors_of_source = source.all_predecessors
            all_successors_of_target = target.all_successors

            all_in_messages = []
            all_out_messages = []

            all_in_messages.extend(source.in_messages)
            all_out_messages.extend(target.out_messages)

            for predecessor in all_predecessors_of_source:
                all_in_messages.extend(predecessor.in_messages)
            for successor in all_successors_of_target:
                all_out_messages.extend(successor.out_messages)

            compact_in_messages = list(set(all_in_messages))
            compact_out_messages = list(set(all_out_messages))

            message.all_predecessor_messages.extend(compact_in_messages)
            message.all_successor_messages.extend(compact_out_messages)

            # message.all_predecessor_messages.sort(key=lambda msg: msg.id, reverse=False)
            # message.all_successor_messages.sort(key=lambda msg: msg.id, reverse=False)

            for predecessor_message in message.all_predecessor_messages:
                message.all_predecessor_messages_lite.append(predecessor_message.name)
            for successor_message in message.all_successor_messages:
                message.all_successor_messages_lite.append(successor_message.name)

    # 标记入口和出口任务, 静态私有方法
    @staticmethod
    def __tag_entry_and_exit_task(app):
        for task in app.tasks:  # 遍历任务集
            if not task.predecessors:  # 如果任务的直接前驱任务集为空, 则
                task.is_entry = True  # 置任务为入口任务
                app.IPPS_entry_task.append(task)  # 同时将任务添加至应用的入口任务集
            if not task.successors:  # 如果任务的直接后继任务集为空, 则
                task.is_exit = True  # 置任务为出口任务
                app.IPPS_exit_task.append(task)  # 同时将任务添加至应用的出口任务集

    @staticmethod
    def __group_task_from_the_top(app):
        app.task_groups_from_the_top.clear()
        groups = app.task_groups_from_the_top       # 取任务分组编号与组的映射
        tasks = app.tasks
        for task in tasks:
            k = SchedulerUtils.get_the_max_steps_to_the_entry(task.predecessors)    # 计算当前任务到入口任务的最长路径
            group = groups.setdefault(k)            # 取任务分组
            if not group:                           # 如果任务分组不存在, 则创建它
                group = TaskGroup(k)                # 创建任务分组
                groups[k] = group

            group.tasks.append(task)                # 将任务加入组

        sorted_task_groups_from_the_top = sorted(groups.items(), key=lambda item: item[0])      # VERY IMPORTANT!!! 对所有任务分组根据组编号从小到大排序
        app.task_groups_from_the_top.clear()        # 清空应用的原始任务分组
        for task_group_id, taskgroup in sorted_task_groups_from_the_top:    # 重新将排序后的任务分组放入应用
            app.task_groups_from_the_top[task_group_id] = taskgroup

    @staticmethod
    def __group_message_from_the_top(app):
        taskgroups = app.task_groups_from_the_top           # 取任务的分组信息
        messagegroups = app.message_groups_from_the_top     # 取消息的分组信息
        for task_group_id, taskgroup in taskgroups.items(): # 遍历任务分组
            messagegroup = messagegroups.setdefault(task_group_id)      # 取当前任务分组编号对应的消息分组
            if not messagegroup:                            # 如果这个消息分组不存在, 则创建它
                messagegroup = MessageGroup(task_group_id)  # 创建消息分组
                messagegroups[task_group_id] = messagegroup # 将分组编号与新创建的消息分组对应起来

            tsk_list = taskgroup.tasks
            for task in tsk_list:                           # 遍历当前任务分组里的所有任务
                for message in task.out_messages:           # 遍历当前任务的所有发送消息
                    messagegroup.messages.append(message)   # 将发送消息加入消息分组

    @staticmethod
    def __group_task_from_the_bottom(app):
        groups = app.task_groups_from_the_bottom
        tasks = app.tasks
        for task in tasks:
            k = SchedulerUtils.get_the_max_steps_to_the_exit(task.successors)
            group = groups.setdefault(k)
            if not group:
                group = TaskGroup(k)
                groups[k] = group

            group.tasks.append(task)
