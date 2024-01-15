#!/usr/bin/env python3
# *-* coding:utf8 *-*

"""
类别: 调度器
名称: 差分进化算法调度器 -- 针对任务的调度
作者: 孙质方
邮件: zf_sun@hnist.edu.cn
日期: 2021年12月10日
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
from time import *
import random
F = 0.5  # 缩放因子
CR = 0.3  # 交叉概率

class EvolutionScheduler(Scheduler):

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
        best_ans=[]
        while k < 300:
            temp_population = []
            mutation_chromosomes = self.mutate(population)  # 个体变异
            crossover_chromosomes = self.crossover(population,mutation_chromosomes)  # 交叉
            population=self.select(self.create_population(app,crossover_chromosomes),population)  # 每次选择种群里适应度值靠前的一半
            population.sort(key=lambda seq: seq.tradeoff)
            # print("<br/>generation = %d, makespan = %.2f, cost = %.2f, time = %s" % (k, population[0].makespan, population[0].cost, datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')))

            best_ans.append(population[0])
            if outfilename == 'Appendix 1.txt':
                k = k + 1
            if outfilename == 'Appendix 3.txt':
                if population[0].makespan <= target:
                    break
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
        #population.sort(key=lambda seq: seq.tradeoff)
        return population

    def create_population(self, app, chromosomes):
        i = 0
        population = []
        candidate_tasks = []
        processor_set = ComputingSystem.processors#处理器
        vrf_set = ComputingSystem.VRFs[0]#电压频率
        while chromosomes:
            self.reset_tasks(app.tasks)
            candidate_tasks.clear()
            candidate_tasks+=app.entry_task#添加入口任务
            chromosome = chromosomes.pop(0)#取出chromosomes种群中第一个个体

            tsk_sequence = []
            prossor_sequence = []
            vrf_sequence=[]
            for j in range(0, len(chromosome)//3):#chromosome整除2
                gene = chromosome[j]
                candidate_tasks.sort(key=lambda tsk: tsk.id)
                size = len(candidate_tasks)#入度为0的任务个数
                # scale = 1.0 / size
                #print('$$$$$$')
                #print(size)
                # tsk_index = self.get_index(gene, scale, size)#???
                tsk_index=int(gene*size)
                task = candidate_tasks[tsk_index]
                task.is_decoded = True
                tsk_sequence.append(task)
                candidate_tasks.remove(task)
                for successor in task.successors:
                    if self.is_ready(successor):
                        candidate_tasks.append(successor)

                prossor_gene = chromosome[j+app.tasknum]
                processor_set.sort(key=lambda prossor: prossor.id)
                # prossor_size = len(processor_set)
                # prossor_scale = 1.0 / prossor_size
                #print(prossor_size)
                # prossor_index = self.get_index(prossor_gene, prossor_scale, prossor_size)
                prossor_index=int(prossor_gene*app.processor_number)
                processor = processor_set[prossor_index]
                prossor_sequence.append(processor)

                vrf_gene = chromosome[2*app.tasknum+j]
                vrf_sequence.append(int(vrf_gene*len(vrf_set)))

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
    #     #print(f'{gene}    {size}   {mid}')
    #     return mid
        # i = 1
        # while i <= size:
        #     if i*scale < gene:
        #         i = i + 1
        #     else:
        #         break
        # return i-1

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

    def select(self, u_list,population):
        for i in range(0, len(population)):
            if u_list[i].tradeoff < population[i].tradeoff:
                population[i] = u_list[i]
        return population

    def crossover(self, population,v_list):
        u_list = []
        for i in range(0, len(population)):
            vv_list = []
            for j in range(0, len(v_list[i])):
                if (random.random() <= CR) | (j == random.randint(0, len(v_list[i]) - 1)):
                    # (j == random.randint(0, len_x - 1)是为了使变异中间体至少有一个基因遗传给下一代
                    vv_list.append(v_list[i][j])
                else:
                    vv_list.append(population[i].chromosome[j])
            u_list.append(vv_list)
        return u_list

    def mutate(self, population):
        v_list = []
        for i in range(0, len(population)):
            r1 = random.randint(0, len(population) - 1)
            while r1 == i:  # r1不能等于i，不能等于i的原因是防止之后进行的交叉操作出现自身和自身交叉的结果
                r1 = random.randint(0, len(population) - 1)
            r2 = random.randint(0, len(population) - 1)
            while r2 == r1 | r2 == i:
                r2 = random.randint(0, len(population) - 1)
            r3 = random.randint(0, len(population) - 1)
            while r3 == r2 | r3 == r1 | r3 == i:
                r3 = random.randint(0, len(population) - 1)
            # 在DE中常见的差分策略是随机选取种群中的两个不同的个体，将其向量差缩放后与待变异个体进行向量合成
            # F为缩放因子F越小，算法对局部的搜索能力更好，F越大算法越能跳出局部极小点，但是收敛速度会变慢。此外，F还影响种群的多样性。
            v_list.append(self.add(population[r1].chromosome, self.multiply(F, self.substract(population[r2].chromosome, population[r3].chromosome))))
        return v_list
        pass

    # 列表相减
    def substract(self,a_list, b_list):
        a = len(a_list)
        new_list = []
        for i in range(0, a):
            b=a_list[i] - b_list[i]
            if b<0:
                b=0
            new_list.append(b)
        return new_list

    # 列表相加
    def add(self,a_list, b_list):
        a = len(a_list)
        new_list = []
        for i in range(0, a):
            b=a_list[i] + b_list[i]
            if b>=1:
                b=0.999999999
            new_list.append(b)
        return new_list

    # 列表的数乘
    def multiply(self,a, b_list):
        b = len(b_list)
        new_list = []
        for i in range(0, b):
            new_list.append(a * b_list[i])
        return new_list