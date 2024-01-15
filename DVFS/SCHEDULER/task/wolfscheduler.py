#!/usr/bin/env python3
# *-* coding:utf8 *-*

"""
类别: 调度器
名称: 灰狼算法调度器 -- 针对任务的调度
作者: 孙质方
邮件: zf_sun@hnist.edu.cn
日期: 2021年12月19日
说明:
"""

import sys
import os
from SCHEDULER.scheduler import Scheduler
from system.computingsystem import ComputingSystem
from UTIL.schedulerutils import SchedulerUtils
from COMPONENT.runningspan import RunningSpan
from COMPONENT.assignment import Assignment
from COMPONENT.assignedprocessor import AssignedProcessor
from COMPONENT.sequence import Sequence
from COMPONENT.schedulinglist import SchedulingList
from UTIL.genericutils import *
from UTIL.logger import Logger
from CONFIG.config import *
from itertools import permutations, product
from datetime import datetime
from copy import *
import random
import numpy
from time import *

class wolfScheduler(Scheduler):

    # sys.stdout = Logger('./result/result_%d.html' % (random.randint(1000, 9999)))
    # sys.stdout = Logger('D:/pycpp/GABUDGET/result/result_task.html')

    #def schedule(self, app,heft_list):
    def schedule(self, app,outfilename,target,st):
        output_path = outfilename
        ComputingSystem.reset(app)  # 重置计算系统. !!!VERY IMPORTANT!!!
        pop_size = 500
        #population = self.init_population(app, pop_size,heft_list)#1000*len(tasks)
        population = self.init_population(app, pop_size)  # 1000*len(tasks)
        k = 0
        Max_iter=300
        best_ans=[]
        while k < Max_iter:
            temp_population = []
            Alpha_pos = population[0].chromosome
            Beta_pos = population[1].chromosome
            Delta_pos = population[2].chromosome
            a = abs(2 - k * ((2) / Max_iter))  # a从2线性减少到0
            for i in range(pop_size):
                temp_chromosome=[]
                for j in range(0, app.tasknum*3):
                    r1 = random.random()  # r1 is a random number in [0,1]主要生成一个0-1的随机浮点数。
                    r2 = random.random()  # r2 is a random number in [0,1]

                    A1 = 2 * a * r1 - a;  # (-a.a)
                    C1 = 2 * r2;  # (0.2)
                    # D_alpha表示候选狼与Alpha狼的距离
                    D_alpha = abs(C1 * Alpha_pos[j] - population[i].chromosome[j]);  # abs() 函数返回数字的绝对值。Alpha_pos[j]表示Alpha位置，Positions[i,j])候选灰狼所在位置
                    X1 = Alpha_pos[j] - A1 * D_alpha;  # X1表示根据alpha得出的下一代灰狼位置向量

                    r1 = random.random()
                    r2 = random.random()

                    A2 = 2 * a * r1 - a;  #
                    C2 = 2 * r2;

                    D_beta = abs(C2 * Beta_pos[j] - population[i].chromosome[j]);
                    X2 = Beta_pos[j] - A2 * D_beta;

                    r1 = random.random()
                    r2 = random.random()

                    A3 = 2 * a * r1 - a;
                    C3 = 2 * r2;

                    D_delta = abs(C3 * Delta_pos[j] - population[i].chromosome[j]);
                    X3 = Delta_pos[j] - A3 * D_delta;

                    temp=(X1 + X2 + X3) / 3
                    if temp<0:
                        temp=0
                    elif temp>=1:
                        temp = 0.99999999
                    temp_chromosome.append(temp)  # 候选狼的位置更新为根据Alpha、Beta、Delta得出的下一代灰狼地址。
                temp_population.append(temp_chromosome)
            population=self.create_population(app,temp_population)
            population.sort(key=lambda seq: seq.tradeoff)
            # print("<br/>generation = %d, makespan = %.2f, cost = %.2f, time = %s" % (k, population[0].makespan, population[0].cost, datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')))

            k = k + 1

            best_ans.append(population[0])
            if outfilename == 'Appendix 3.txt':
                if population[0].makespan <= target:
                    break
                else:
                    Max_iter=Max_iter+0.3  #防止算法在300次迭代之后没有收敛到目标值
            if outfilename == 'Appendix 4.txt':
                T = time()
                if T - st >= target:
                    break

        # print("-" * 100)
        # print("<br/>pop_size = %d<br/>" % pop_size)
        elite_sequence = population[0]
        makespan = elite_sequence.makespan#调度序列完工时间
        # print(list(ii.id for ii in elite_sequence.tsk_sequence))
        # print(list(ii.id for ii in elite_sequence.prossor_sequence))
        # cost = elite_sequence.cost        #调度序列总成本
        # tradeoff = ALPHA * makespan + BETA * cost
        if outfilename == 'Appendix 1.txt':
            with open(output_path, 'a', encoding='utf-8') as file1:
                print(list(best_ans[i].makespan for i in range(k)), file=file1)
            print(list(best_ans[i].makespan for i in range(k)))

        output_path = outfilename
        with open(output_path, 'a', encoding='utf-8') as file1:
            print("The scheduler = %s, makespan = %.2f, allE = %.2f, tradeoff = %.2f" % (
                self.scheduler_name, makespan, elite_sequence.allE, elite_sequence.tradeoff), file=file1)
        print("The scheduler = %s, makespan = %.2f, allE = %.2f, tradeoff = %.2f" % (
            self.scheduler_name, makespan, elite_sequence.allE, elite_sequence.tradeoff))

        return makespan#, cost

    #def init_population(self, app, pop_size,heft_list):
    def init_population(self, app, pop_size):
        chromosomes = []
        tasks = app.tasks

        for i in range(0, pop_size):  #种群数量1000
            chromosome = []
            for j in range(0, 3*app.tasknum):
                chromosome.append(random.random())
            chromosomes.append(chromosome)
        #gene_list=self.re_index()
        population = self.create_population(app, chromosomes)#1000*len(tasks)
        population.sort(key=lambda seq: seq.tradeoff)
        return population

    def create_population(self, app, chromosomes):
        i = 0
        population = []
        candidate_tasks = []
        processor_set = ComputingSystem.processors  # 处理器
        vrf_set = ComputingSystem.VRFs[0]  # 电压频率
        while chromosomes:
            self.reset_tasks(app.tasks)
            candidate_tasks.clear()
            candidate_tasks += app.entry_task  # 添加入口任务
            chromosome = chromosomes.pop(0)  # 取出chromosomes种群中第一个个体

            tsk_sequence = []
            prossor_sequence = []
            vrf_sequence = []
            for j in range(0, len(chromosome) // 3):  # chromosome整除2
                gene = chromosome[j]
                candidate_tasks.sort(key=lambda tsk: tsk.id)
                size = len(candidate_tasks)  # 入度为0的任务个数
                # scale = 1.0 / size
                # print('$$$$$$')
                # print(size)
                # tsk_index = self.get_index(gene, scale, size)#???
                tsk_index = int(gene * size)
                task = candidate_tasks[tsk_index]
                task.is_decoded = True
                tsk_sequence.append(task)
                candidate_tasks.remove(task)
                for successor in task.successors:
                    if self.is_ready(successor):
                        candidate_tasks.append(successor)

                prossor_gene = chromosome[j + app.tasknum]
                processor_set.sort(key=lambda prossor: prossor.id)
                # prossor_size = len(processor_set)
                # prossor_scale = 1.0 / prossor_size
                # print(prossor_size)
                # prossor_index = self.get_index(prossor_gene, prossor_scale, prossor_size)
                prossor_index = int(prossor_gene * app.processor_number)
                processor = processor_set[prossor_index]
                prossor_sequence.append(processor)

                vrf_gene = chromosome[2 * app.tasknum + j]
                vrf_sequence.append(int(vrf_gene * len(vrf_set)))

            makespan, scheduling_list = self.calculate_response_time_and_cost(app, i, tsk_sequence, prossor_sequence,
                                                                              vrf_sequence)
            # print(scheduling_list.allE)
            # print(prossor_sequence)
            i = i + 1
            s = Sequence(chromosome, tsk_sequence, prossor_sequence, makespan, scheduling_list.allE)
            s.scheduling_list = scheduling_list
            population.append(s)

        return population

    def reset_tasks(self, tasks):
        for task in tasks:
            task.is_decoded = False

    def is_ready(self, task):
        for predecessor in task.predecessors:
            if not predecessor.is_decoded:
                return False
        return True

    # def get_index(self, gene, scale, size):#gene：个体的基因，scale=1/size
    #     l = 0
    #     r = size
    #     mid = (l + r) // 2
    #     while l <= r:
    #         temp = mid * scale
    #         if temp < gene:
    #             l = mid + 1
    #         elif temp > gene:
    #             r = mid - 1
    #         else:
    #             return mid
    #         mid = (l + r) // 2
    #     return mid


    # def re_index(self,heft_list,scale):
    #     gene_list=[]
    #     for i in heft_list:
    #         k=i
    #         gene=k*scale
    #         gene_list.append(gene)
    #     return gene_list

    def calculate_response_time_and_cost(self, app, counter, task_sequence, processor_sequence, vrf_sequence):
        ComputingSystem.reset(app)  # 重置计算系统. !!!VERY IMPORTANT!!!
        processors = ComputingSystem.processors1  # 处理器集
        vrf_set = ComputingSystem.VRFs[0]  # 电压频率

        scheduling_list = self.scheduling_lists.setdefault(counter)  # 判断字典scheduling_lists里是否有键counter，没有自动添加

        if not scheduling_list:
            scheduling_list = SchedulingList("Scheduling_List_%d" % counter)
            # self.scheduling_lists[counter] = scheduling_list

        for i in range(0, app.tasknum):  # 遍历当前消息分组内的所有消息
            task = task_sequence[i]  # 取任务 task
            processor = processor_sequence[i]  # 取任务 task 对应的运行处理器 processor
            vrf = vrf_set[vrf_sequence[i]]

            start_time = SchedulerUtils.calculate_earliest_start_time(task, processor)  # 当前遍历处理器上最早可用启动时间
            finish_time = start_time + task.processor__computation_time[processor]  # 当前遍历处理器上最早可用结束时间

            running_span = RunningSpan(start_time, finish_time)  # 上述 for 循环结束后, 最合适的处理器已被找出, 此时可以记录下任务的运行时间段
            assignment = AssignedProcessor(processor, vrf, running_span)  # 同时记录下任务的运行时环境
            # assignment = Assignment(processor, running_span)  # 同时记录下任务的运行时环境

            task.assignment = assignment  # 设置任务的运行时环境

            task.is_assigned = True  # 标记任务已被分配

            processor.resident_tasks.append(task)  # 将任务添加至处理器的驻留任务集中
            processor.resident_tasks.sort(
                key=lambda tsk: tsk.assignment.running_span.start_time)  # 对处理器的驻留任务进行排序, 依据任务启动时间升序排列

            scheduling_list.list[task] = assignment  # 将任务与对应运行时环境置于原始调度列表

        makespan = calculate_makespan(scheduling_list)
        # cost = calculate_cost(self.scheduling_lists[counter])
        scheduling_list.makespan = makespan  # 计算原始调度列表的完工时间
        allE = consumeEnergyInVRF(processors, scheduling_list, makespan)
        scheduling_list.allE = allE
        # self.scheduling_lists[counter].cost = cost

        # print("The scheduler = %s, list_name = %s, makespan = %.2f" % (self.scheduler_name,
        #                                                                self.scheduling_lists[counter].list_name,
        #                                                                self.scheduling_lists[counter].makespan))

        # if SHOW_ORIGINAL_SCHEDULING_LIST:  # 如果打印原始调度列表, 则:
        #     print_scheduling_list(self.scheduling_lists[counter])  # 打印原始调度列表

        # if makespan < 100.0:
        #     for task in self.scheduling_lists[counter].list.keys():
        #         info = "%s\t%s\t%s" % (task.name, task.assignment.assigned_processor.name, task.assignment.running_span)
        #         print(info)
        #     print("-" * 100)
        #     print("The scheduler = %s, list_name = %s, makespan = %.2f<br/>" % (self.scheduler_name, self.scheduling_lists[counter].list_name, self.scheduling_lists[counter].makespan))
        #     print("#" * 100)
        # else:
        #     print("The scheduler = %s, list_name = %s, makespan = %.2f<br/>" % (self.scheduler_name, self.scheduling_lists[counter].list_name, self.scheduling_lists[counter].makespan))

        # self.scheduling_lists.clear()
        return makespan, scheduling_list  # , cost