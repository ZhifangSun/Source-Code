#!/usr/bin/env python3
# *-* coding:utf8 *-*

"""
类别: 工具组件
名称: 调度器工具类
作者: strong
邮件: jqjiang@hnist.edu.cn
日期: 2020年3月23日
说明: 专门放置作用于调度器的工具函数的类
"""

from datetime import datetime
from copy import *
import random


class SchedulerUtils(object):

    # 计算实参任务在处理器上最早启动时间, 类方法
    @classmethod
    def calculate_earliest_start_time(cls, task, processor):

        predecessor_available_time = 0.0  # 变量, 用于记录前驱任务的最早可用时间
        processor_available_time = 0.0  # 变量, 用于记录处理器的最早可用时间

        resident_tasks = processor.resident_tasks  # 处理器的驻留任务集

        if resident_tasks:  # 如果驻留任务集不为空, 则:
            for t in resident_tasks:  # 遍历驻留任务集
                if t.application == task.application:  # 如果当前遍历驻留任务与实参任务属同一应用, 则:
                    temp_finish_time = t.assignment.running_span.finish_time
                    if processor_available_time < temp_finish_time:
                        processor_available_time = temp_finish_time  # 设置处理器的最早可用时间为最后一个驻留任务的结束时间

        if task.is_entry:  # 如果实参任务为入口任务, 则:
            earliest_start_time = processor_available_time  # 设置最早启动时间为处理器的最早可用时间
        else:  # 如果实参任务不为入口任务, 则:
            for predecessor in task.predecessors:  # 遍历实参任务的直接前驱任务集
                assigned_processor_of_predecessor = predecessor.assignment.assigned_processor  # 取前驱任务所分配运行处理器
                if processor == assigned_processor_of_predecessor:  # 如果实参处理器与前驱任务所分配运行处理器为同一处理器, 则:
                    communication_time = 0.0  # 置通信时间为 0
                else:  # 如果实参处理器与前驱任务所分配运行处理器不为同一处理器, 则:
                    communication_time = task.predecessor__communication_time[predecessor]  # 置通信时间为二者之间的通信时间

                finish_time_of_predecessor = predecessor.assignment.running_span.finish_time  # 取前驱任务的运行结束时间

                if (finish_time_of_predecessor + communication_time) > predecessor_available_time:  # 如果前驱任务运行结束时间加上通信时间大于此时前驱任务的最早可用时间, 则:
                    predecessor_available_time = finish_time_of_predecessor + communication_time  # 置前驱任务的最早可用时间为前驱任务运行结束时间与通信时间之和

            earliest_start_time = processor_available_time if processor_available_time > predecessor_available_time else predecessor_available_time  # 取前驱任务最早可用时间和处理器最早可用时间二者中最大值为实参任务最早启动时间

        return earliest_start_time  # 返回最早启动时间

    @classmethod  # IPPS专用方法
    def IPPS_calculate_earliest_start_time(cls, task, processor, chromosome_dex):

        predecessor_available_time = 0.0  # 变量, 用于记录前驱任务的最早可用时间
        processor_available_time = 0.0  # 变量, 用于记录处理器的最早可用时间

        resident_tasks = processor.resident_tasks  # 处理器的驻留任务集

        if resident_tasks:  # 如果驻留任务集不为空, 则:
            for t in resident_tasks:  # 遍历驻留任务集
                if t.application == task.application:  # 如果当前遍历驻留任务与实参任务属同一应用, 则:
                    temp_finish_time = t.assignment.running_span.finish_time
                    if processor_available_time < temp_finish_time:
                        processor_available_time = temp_finish_time  # 设置处理器的最早可用时间为最后一个驻留任务的结束时间

        if task.is_entry:  # 如果实参任务为入口任务, 则:
            earliest_start_time = processor_available_time  # 设置最早启动时间为处理器的最早可用时间
        else:  # 如果实参任务不为入口任务, 则:
            for predecessor in task.predecessors:  # 遍历实参任务的直接前驱任务集
                if predecessor.id not in chromosome_dex:
                    continue
                assigned_processor_of_predecessor = predecessor.assignment.assigned_processor  # 取前驱任务所分配运行处理器
                if processor == assigned_processor_of_predecessor:  # 如果实参处理器与前驱任务所分配运行处理器为同一处理器, 则:
                    communication_time = 0.0  # 置通信时间为 0
                else:  # 如果实参处理器与前驱任务所分配运行处理器不为同一处理器, 则:
                    communication_time = task.predecessor__communication_time[predecessor]  # 置通信时间为二者之间的通信时间

                finish_time_of_predecessor = predecessor.assignment.running_span.finish_time  # 取前驱任务的运行结束时间

                if (
                        finish_time_of_predecessor + communication_time) > predecessor_available_time:  # 如果前驱任务运行结束时间加上通信时间大于此时前驱任务的最早可用时间, 则:
                    predecessor_available_time = finish_time_of_predecessor + communication_time  # 置前驱任务的最早可用时间为前驱任务运行结束时间与通信时间之和

            earliest_start_time = processor_available_time if processor_available_time > predecessor_available_time else predecessor_available_time  # 取前驱任务最早可用时间和处理器最早可用时间二者中最大值为实参任务最早启动时间

        return earliest_start_time  # 返回最早启动时间

    # 计算实参任务在处理器上最早结束时间, 类方法
    @classmethod
    def calculate_earliest_finish_time(cls, task, processor):
        earliest_start_time = cls.calculate_earliest_start_time(task, processor)
        computation_time = task.processor__computation_time[processor]
        earliest_finish_time = earliest_start_time + computation_time
        return earliest_finish_time

    @classmethod
    def get_the_mini_computation_time_processor(cls, tasks, processors):
        processor = None

        min_computation_time = float("inf")

        for p in processors:
            computation_time = 0.0
            for task in tasks:
                computation_time += task.processor__computation_time[p]

            if min_computation_time > computation_time:
                min_computation_time = computation_time
                processor = p

        return processor

    @classmethod
    def is_ready(cls, task):
        flag = True
        if task.predecessors:
            for predecessor in task.predecessors:
                flag = flag and predecessor.is_assigned

        return flag

    @classmethod
    def get_the_max_steps_to_the_entry(cls, predecessors):
        max_steps = 0

        if not predecessors:
            max_steps = 0
        else:
            for predecessor in predecessors:
                steps = cls.get_the_max_steps_to_the_entry(predecessor.predecessors) + 1
                if steps > max_steps:
                    max_steps = steps

        return max_steps

    @classmethod
    def get_the_max_steps_to_the_exit(cls, successors):
        max_steps = 0

        if not successors:
            max_steps = 0
        else:
            for successor in successors:
                steps = cls.get_the_max_steps_to_the_exit(successor.successors) + 1
                if steps > max_steps:
                    max_steps = steps

        return max_steps
    '''
    @classmethod
    def get_predecessor_messages(cls, message):
        source = message.source
        if source.is_entry:
            return []
        else:
            predecessor_messages = source.in_messages
            if predecessor_messages:
                for predecessor_message in predecessor_messages:
                    predecessor_messages.extend(cls.get_predecessor_messages(predecessor_message))
            return predecessor_messages

    @classmethod
    def get_predecessor_messages2(cls, message):
        immediate_predecessor_messages = message.immediate_predecessor_messages
        if immediate_predecessor_messages:
            all_predecessor_messages = immediate_predecessor_messages
            for predecessor_message in immediate_predecessor_messages:
                all_predecessor_messages.extend(cls.get_predecessor_messages2(predecessor_message))
            return all_predecessor_messages
        else:
            return []

    @classmethod
    def get_predecessor_messages3(cls, message):
        immediate_predecessor_messages = message.immediate_predecessor_messages
        if immediate_predecessor_messages:
            message.all_predecessor_messages.extend(immediate_predecessor_messages)
            for predecessor_message in immediate_predecessor_messages:
                if predecessor_message.all_predecessor_messages:
                    message.all_predecessor_messages.extend(predecessor_message.all_predecessor_messages)
        else:
            message.all_predecessor_messages.extend([])
            print("--------")

    @classmethod
    def get_successor_messages(cls, message):
        target = message.target
        # print("message = %s, target = %s" % (message, target))
        if target.is_exit:
            return []
        else:
            successor_messages = target.out_messages
            if successor_messages:
                for successor_message in successor_messages:
                    successor_messages.extend(cls.get_successor_messages(successor_message))
            return successor_messages
    '''

    @classmethod
    def find_message_by_name(cls, messages, name):
        for msg in messages:
            if msg.name == name:
                return msg

    @classmethod
    def has_predecessor(cls, message, rear):
        flag = False
        predecessors = message.all_predecessor_messages_lite
        for msg in rear:
            if msg in predecessors:
                flag = True
        return flag

    @classmethod
    def has_successor(cls, message, head):
        flag = False
        successors = message.all_successor_messages_lite
        for msg in head:
            if msg in successors:
                flag = True
        return flag

    @classmethod
    def swap(cls, msg_list, i, j):
        msg = msg_list[i]
        msg_list[i] = msg_list[j]
        msg_list[j] = msg

    @classmethod
    def generate_valid_sequences(cls, app, messages, messages_lite, begin, end):
        if begin == end:
            include = True
            for i in range(len(messages_lite)):
                i_msg = SchedulerUtils.find_message_by_name(messages, messages_lite[i])
                for j in range((i+1), len(messages_lite)):
                    j_msg = SchedulerUtils.find_message_by_name(messages, messages_lite[j])
                    if j_msg in i_msg.all_predecessor_messages or i_msg in j_msg.all_successor_messages:
                        include = False
                        break
                if not include:
                    break
            if include:
                msg_sequence = deepcopy(messages_lite)
                app.sequences.append(msg_sequence)
                print("%d ---- %s ---- %s" % (len(app.sequences), (datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')), msg_sequence))
            pass

        for i in range(begin, (end+1)):
            cls.swap(messages_lite, begin, i)
            cls.generate_valid_sequences(app, messages, messages_lite, begin+1, end)
            cls.swap(messages_lite, begin, i)
            pass

    @classmethod
    def init_population(cls, app, messages, messages_lite, begin, end, size):
        if begin == end:
            include = True
            for i in range(len(messages_lite)):
                i_msg = SchedulerUtils.find_message_by_name(messages, messages_lite[i])
                for j in range((i + 1), len(messages_lite)):
                    j_msg = SchedulerUtils.find_message_by_name(messages, messages_lite[j])
                    if j_msg in i_msg.all_predecessor_messages or i_msg in j_msg.all_successor_messages:
                        include = False
                        break
                if not include:
                    break
            if include:
                msg_sequence = deepcopy(messages_lite)
                app.sequences.append(msg_sequence)
                count = len(app.sequences)
                if count > size:
                    return
                # print("%d ---- %s ---- %s" % (len(app.sequences), (datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')), msg_sequence))
            pass

        for i in range(begin, (end + 1)):
            cls.swap(messages_lite, begin, i)
            cls.init_population(app, messages, messages_lite, begin + 1, end, size)
            cls.swap(messages_lite, begin, i)
            pass

    @classmethod
    def generateComputationMatrix(cls,taskNumber, processorNumber):
        computationMatrix=[]
        upper = 20
        lower = 5
        for i in range(taskNumber):
            temp=[]
            for j in range(processorNumber):
                v=lower+random.randint(0,upper)
                cost=float(v)
                temp.append(cost)
            computationMatrix.append(temp)
        return computationMatrix

    @classmethod
    def generateCommunicationMatrixGaussian(cls,m):
        taskNumber = int((m * m + m - 2) / 2)
        communicationMatrix=[]
        upper = 27
        lower = 10

        end = m - 1
        k = 2
        level = m - 1
        for i in range(taskNumber):
            temp=[]
            for j in range(taskNumber):
                temp.append(0.0)
                if i==0 and (j>0 and j<m):
                    temp[j]=float(lower+random.randint(0,upper))
            communicationMatrix.append(temp)
        for i in range(taskNumber):
            for j in range(i,taskNumber):
                if i==end+1:
                    for a in range(i+1,i+1+m-k):
                        communicationMatrix[i][a]=float(lower+random.randint(0,upper))
                    end=end+1+(m-k)
                    k=k+1
                    level=level-1
                    break
                if i>0 and j==(i+level):
                    communicationMatrix[i][j] = float(lower + random.randint(0, upper))
        return communicationMatrix