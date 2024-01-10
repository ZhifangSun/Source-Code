#!/usr/bin/env python3
# *-* coding:utf8 *-*

"""
类别: 调度器
名称: NGA算法调度器 -- 针对任务的调度
作者: 孙质方
邮件: zf_sun@vip.hnist.edu.cn
日期: 2022年5月10日
说明:
"""

import sys
import os
from SCHEDULER.scheduler import Scheduler
from system.computingsystem import ComputingSystem
from UTIL.schedulerutils import SchedulerUtils
from COMPONENT.runningspan import RunningSpan
from COMPONENT.assignment import Assignment
from COMPONENT.sequence import Sequence
from COMPONENT.schedulinglist import SchedulingList
from UTIL.genericutils import *
from UTIL.logger import Logger
from CONFIG.config import *
from itertools import permutations, product
from datetime import datetime
from copy import *
from time import *


import sys
import os
from SCHEDULER.scheduler import Scheduler
from system.computingsystem import ComputingSystem
from UTIL.schedulerutils import SchedulerUtils
from COMPONENT.runningspan import RunningSpan
from COMPONENT.assignment import Assignment
from COMPONENT.sequence import Sequence
from COMPONENT.schedulinglist import SchedulingList
from UTIL.genericutils import *
from UTIL.logger import Logger
from CONFIG.config import *
from itertools import permutations, product
from datetime import datetime
from copy import *
import random
import matplotlib.pyplot as plt
import numpy as np


class NGAScheduler(Scheduler):

    # sys.stdout = Logger('./result/result_%d.html' % (random.randint(1000, 9999)))
    sys.stdout = Logger('D:/pycpp/GABUDGET/result/result_task.html')

    def schedule(self, sign,app,outfilename,target,st):
        output_path = outfilename
        ComputingSystem.reset(app)  # 重置计算系统. !!!VERY IMPORTANT!!!
        pop_size = 500
        EliteRate=0.2
        MutationRate=0.02
        Elitepop=int(pop_size*EliteRate)#精英种群
        population = self.init_population(app, pop_size)
        k = 0
        best_ans=[]
        while k < 300:
            half_population = []
            # half_population.extend(self.select(population,Elitepop))#每次选择种群里适应度值靠前的精英种群
            crossover_chromosomes = self.crossover(app,pop_size,population,Elitepop)#前后交叉
            for i in range(0,Elitepop):
                Elich=population[i].chromosome.copy()
                crossover_chromosomes.insert(0,Elich)
            # population = self.create_population(app, crossover_chromosomes)
            mutation_chromosomes = self.mutate(app,pop_size,crossover_chromosomes,MutationRate)#个体变异
            population=self.create_population(app,mutation_chromosomes)
            population.sort(key=lambda seq: seq.makespan)
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
        cost = elite_sequence.cost#调度序列总成本
        # print(list(ii.id for ii in elite_sequence.tsk_sequence))
        # print(list(ii.id for ii in elite_sequence.prossor_sequence))
        # tradeoff = ALPHA * makespan + BETA * cost
        if outfilename == 'Appendix 1.txt':
            with open(output_path, 'a', encoding='utf-8') as file1:
                print(list(best_ans[i].makespan for i in range(k)), file=file1)
            print(list(best_ans[i].makespan for i in range(k)))

        output_path = outfilename
        with open(output_path, 'a', encoding='utf-8') as file1:
            print("The scheduler = %s, makespan = %.2f" % (self.scheduler_name, makespan), file=file1)
        print("The scheduler = %s, makespan = %.2f" % (self.scheduler_name, makespan))

        # print("The scheduler = %s, makespan = %.2f, cost = %.2f, tradeoff = %.2f, slr = %.2f, mcr = %.2f" % (self.scheduler_name,
        #                                                                             makespan, cost, tradeoff,
        #                                                                             makespan / app.cp_min_time,
        #                                                                             cost / app.cp_min_cost))
        if sign <= 10:
            complete_time = {}
            lists=elite_sequence.scheduling_list
            for i in elite_sequence.tsk_sequence:
                start_time = lists.list[i].running_span.start_time
                finish_time = lists.list[i].running_span.finish_time
                span = lists.list[i].running_span.span
                id = (elite_sequence.tsk_sequence[elite_sequence.tsk_sequence.index(i)].id,
                      elite_sequence.prossor_sequence[elite_sequence.tsk_sequence.index(i)].id)
                complete_time[id] = (start_time, finish_time, span)
            # print(complete_time)

            colors = {}
            col=0
            for i in range(1,app.tasknum+1):
                colors[i]=col
                col+=1
                if col>7:
                    col=0
            e = 255
            color = [(144 / e, 201 / e, 231 / e), (33 / e, 158 / e, 188 / e), (19 / e, 103 / e, 131 / e),
                     (21 / e, 151 / e, 165 / e), (254 / e, 183 / e, 5 / e), (243 / e, 162 / e, 97 / e),
                     (250 / e, 134 / e, 0 / e), (233 / e, 196 / e, 107 / e)]
            for k, v in complete_time.items():
                plt.barh(y=k[1], width=v[2], left=v[0], edgecolor="black", color=color[colors[k[0]]])
                plt.text(v[0] + 0.2, k[1], 't' + str(k[0] - 1), fontsize=10, verticalalignment="center")
                # plt.text(v[0] + 0.2, 2 * k[2] - 0.2, str(v[0]) + " " + str(v[1]), fontdict=fontdict_time)

            my_y_ticks = np.arange(1, app.processor_number + 1, 1)  # 原始数据有13个点，故此处为设置从0开始，间隔为1

            plt.yticks(my_y_ticks)
            plt.title("Gantt chart")
            plt.xlabel("makespan")
            plt.ylabel("processor")
            plt.vlines(elite_sequence.makespan, 0, app.processor_number + 1, colors='black',
                       label="makespan=" + str(int(elite_sequence.makespan)))
            plt.legend(bbox_to_anchor=(0.68, 1.01), loc=3, borderaxespad=0)

            plt.gca().margins(x=0)
            plt.gcf().canvas.draw()

            # set size
            maxsize = 100
            m = 0.2
            N = len(complete_time)
            s = maxsize / plt.gcf().dpi * N + 2 * m
            margin = m / plt.gcf().get_size_inches()[0]

            plt.gcf().subplots_adjust(left=margin, right=1. - margin)
            plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])
            # plt.savefig("C:\\Users\\85184\\Desktop\\Ganttecs.pdf", format='pdf')
            plt.show()
        return makespan, cost

    def init_population(self, app, pop_size):
        chromosomes = []
        uprank_tasks = app.tasks.copy()
        uprank_tasks.sort(key=lambda seq: seq.rank_up_value,reverse=True)
        # print(list(idd.id for idd in uprank_tasks))
        chromosomes.append(uprank_tasks)

        downrank_tasks = app.tasks.copy()
        downrank_tasks.sort(key=lambda seq: seq.rank_down_value)
        # print(list(idd.id for idd in downrank_tasks))
        chromosomes.append(downrank_tasks)

        candidate_tasks = []
        candidate_tasks += app.entry_task  # 添加入口任务
        udrank_tasks = []
        for j in range(0, app.tasknum):
            candidate_tasks.sort(key=lambda tsk: tsk.rank_sum_value,reverse=True)
            task = candidate_tasks[0]
            udrank_tasks.append(task)
            task.is_decoded = True
            candidate_tasks.remove(task)
            for successor in task.successors:
                if self.is_ready(successor):
                    candidate_tasks.append(successor)
        # print(list(idd.id for idd in udrank_tasks))
        chromosomes.append(udrank_tasks)


        for i in range(0, pop_size-3):
            chromosome = []
            self.reset_tasks(app.tasks)
            candidate_tasks.clear()
            candidate_tasks+=app.entry_task#添加入口任务
            for j in range(0, app.tasknum):
                candidate_tasks.sort(key=lambda tsk: tsk.id)
                task=candidate_tasks[random.randint(0,len(candidate_tasks)-1)]
                # print(task.id,end=' ')
                chromosome.append(task)
                task.is_decoded = True
                candidate_tasks.remove(task)
                for successor in task.successors:
                    if self.is_ready(successor):
                        candidate_tasks.append(successor)
            # print()
            chromosomes.append(chromosome)

        population = self.create_population(app, chromosomes)#1000*len(tasks)
        population.sort(key=lambda seq: seq.makespan)
        return population

    def create_population(self, app, chromosomes):
        i = 0
        population = []
        processor_set = ComputingSystem.processors#处理器
        while chromosomes:
            # print(i)
            ComputingSystem.reset(app)  # 重置计算系统. !!!VERY IMPORTANT!!!

            chromosome = chromosomes.pop(0)
            tsk_sequence=chromosome
            prossor_sequence = []
            processor = None  # 全局处理器

            scheduling_list = self.scheduling_lists.setdefault(i)  # 判断字典scheduling_lists里是否有键counter，没有自动添加
            # print(list(idd.id for idd in app.entry_task))
            if not scheduling_list:
                scheduling_list = SchedulingList("Scheduling_List_%d" % i)

            # print(list(ii.id for ii in tsk_sequence))
            for task in tsk_sequence:  # 遍历排序
                earliest_start_time = 0.0  # 初始化全局最早启动时间为0
                earliest_finish_time = float("inf")  # 初始化全局最早结束时间为无穷大
                for p in processor_set:  # 遍历处理器集
                    earliest_start_time_of_this_processor = SchedulerUtils.calculate_earliest_start_time(task,p)  # 当前遍历处理器上最早可用启动时间
                    earliest_finish_time_of_this_processor = earliest_start_time_of_this_processor + \
                                                             task.processor__computation_time[p]  # 当前遍历处理器上最早可用结束时间
                    # print('!!!')
                    if earliest_finish_time > earliest_finish_time_of_this_processor:  # 如果全局最早启动时间大于当前遍历处理器上最早可用启动时间, 则
                        earliest_start_time = earliest_start_time_of_this_processor  # 设置全局最早启动时间为当前遍历处理器上最早可用启动时间
                        earliest_finish_time = earliest_finish_time_of_this_processor  # 设置全局最早结束时间为当前遍历处理器上最早可用结束时间
                        processor = p  # 设置全局处理器为当前遍历处理器
                prossor_sequence.append(processor)
                running_span = RunningSpan(earliest_start_time,
                                           earliest_finish_time)  # 上述 for 循环结束后, 最合适的处理器已被找出, 此时可以记录下任务的运行时间段
                assignment = Assignment(processor, running_span)  # 同时记录下任务的运行时环境

                task.assignment = assignment  # 设置任务的运行时环境

                task.is_assigned = True  # 标记任务已被分配

                processor.resident_tasks.append(task)  # 将任务添加至处理器的驻留任务集中
                processor.resident_tasks.sort(
                    key=lambda tsk: tsk.assignment.running_span.start_time)  # 对处理器的驻留任务进行排序, 依据任务启动时间升序排列

                scheduling_list.list[task] = assignment  # 将任务与对应运行时环境置于原始调度列表
            makespan = calculate_makespan(scheduling_list)

            i = i + 1
            s = Sequence(chromosome, tsk_sequence, prossor_sequence, makespan)
            s.scheduling_list=scheduling_list
            population.append(s)

        return population#,self.scheduling_lists

    def reset_tasks(self, tasks):
        for task in tasks:
            task.is_decoded = False

    def is_ready(self, task):
        for predecessor in task.predecessors:
            if not predecessor.is_decoded:
                return False
        return True


    # def calculate_response_time_and_cost(self, app, counter, task_sequence, processor_sequence):
    #     ComputingSystem.reset(app)  # 重置计算系统. !!!VERY IMPORTANT!!!
    #
    #     scheduling_list = self.scheduling_lists.setdefault(counter)#判断字典scheduling_lists里是否有键counter，没有自动添加
    #
    #     if not scheduling_list:
    #         scheduling_list = SchedulingList("Scheduling_List_%d" % counter)
    #         # self.scheduling_lists[counter] = scheduling_list
    #
    #     for i in range(0, len(task_sequence)):  # 遍历当前消息分组内的所有消息
    #         task = task_sequence[i]  # 取任务 task
    #         processor = processor_sequence[i]  # 取任务 task 对应的运行处理器 processor
    #
    #         start_time = SchedulerUtils.calculate_earliest_start_time(task, processor)  # 当前遍历处理器上最早可用启动时间
    #         finish_time = start_time + task.processor__computation_time[processor]  # 当前遍历处理器上最早可用结束时间
    #
    #         running_span = RunningSpan(start_time, finish_time)  # 上述 for 循环结束后, 最合适的处理器已被找出, 此时可以记录下任务的运行时间段
    #         assignment = Assignment(processor, running_span)  # 同时记录下任务的运行时环境
    #
    #         task.assignment = assignment  # 设置任务的运行时环境
    #
    #         task.is_assigned = True  # 标记任务已被分配
    #
    #         processor.resident_tasks.append(task)  # 将任务添加至处理器的驻留任务集中
    #         processor.resident_tasks.sort(key=lambda tsk: tsk.assignment.running_span.start_time)  # 对处理器的驻留任务进行排序, 依据任务启动时间升序排列
    #
    #         scheduling_list.list[task] = assignment  # 将任务与对应运行时环境置于原始调度列表
    #
    #     makespan = calculate_makespan(scheduling_list)
    #     # cost = calculate_cost(self.scheduling_lists[counter])
    #     scheduling_list.makespan = makespan  # 计算原始调度列表的完工时间
    #     # self.scheduling_lists[counter].cost = cost
    #
    #     # print("The scheduler = %s, list_name = %s, makespan = %.2f" % (self.scheduler_name,
    #     #                                                                self.scheduling_lists[counter].list_name,
    #     #                                                                self.scheduling_lists[counter].makespan))
    #
    #     # if SHOW_ORIGINAL_SCHEDULING_LIST:  # 如果打印原始调度列表, 则:
    #     #     print_scheduling_list(self.scheduling_lists[counter])  # 打印原始调度列表
    #
    #     # if makespan < 100.0:
    #     #     for task in self.scheduling_lists[counter].list.keys():
    #     #         info = "%s\t%s\t%s" % (task.name, task.assignment.assigned_processor.name, task.assignment.running_span)
    #     #         print(info)
    #     #     print("-" * 100)
    #     #     print("The scheduler = %s, list_name = %s, makespan = %.2f<br/>" % (self.scheduler_name, self.scheduling_lists[counter].list_name, self.scheduling_lists[counter].makespan))
    #     #     print("#" * 100)
    #     # else:
    #     #     print("The scheduler = %s, list_name = %s, makespan = %.2f<br/>" % (self.scheduler_name, self.scheduling_lists[counter].list_name, self.scheduling_lists[counter].makespan))
    #
    #     # self.scheduling_lists.clear()
    #     return makespan,scheduling_list#, cost


    def crossover(self, app,pop_size, population,Elitepop):
        flag=True
        offspring_population = []
        for i in range(Elitepop, pop_size):
            prev_chromosome1=[]
            next_chromosome1 = []
            prev_chromosome2 = []
            next_chromosome2 = []
            pop1=random.randint(0,pop_size-1)
            pop2=random.randint(Elitepop+1,pop_size-1)
            while pop2==pop1:
                pop1 = random.randint(0, pop_size-1)
            crossover_point = random.randint(1, app.tasknum-2)
            prev_chromosome1.extend(population[pop1].chromosome)
            next_chromosome1.extend(population[pop2].chromosome)
            prev_chromosome2.extend(population[pop1].chromosome)
            next_chromosome2.extend(population[pop2].chromosome)

            # print(crossover_point)
            # print(list(ii.id for ii in prev_chromosome1))
            # print(list(ii.id for ii in next_chromosome1))
            # print(list(ii.id for ii in prev_chromosome2))
            # print(list(ii.id for ii in next_chromosome2))
            # print('@#@#')

            temp_l = prev_chromosome1.copy()
            delta=app.tasknum-1
            for j in range(app.tasknum-1,-1,-1):
                fd=False
                for k in range(crossover_point,-1,-1):
                    if next_chromosome1[j]==prev_chromosome1[k]:
                        fd=True
                        break
                if not fd:
                    prev_chromosome1[delta]=next_chromosome1[j]
                    delta-=1
                    if delta<=crossover_point:
                        break
            delta=app.tasknum-1
            for j in range(app.tasknum - 1, -1, -1):
                fd = False
                for k in range(crossover_point, -1, -1):
                    if temp_l[j] == next_chromosome1[k]:
                        fd = True
                        break
                if not fd:
                    next_chromosome1[delta] = temp_l[j]
                    delta -= 1
                    if delta <= crossover_point:
                        break

            temp_l = prev_chromosome2.copy()
            delta = 0
            for j in range(0,app.tasknum):
                fd = False
                for k in range(crossover_point , app.tasknum):
                    if next_chromosome2[j] == prev_chromosome2[k]:
                        fd = True
                        break
                if not fd:
                    prev_chromosome2[delta] = next_chromosome2[j]
                    delta += 1
                    if delta >= crossover_point:
                        break
            delta = 0
            for j in range(0,app.tasknum):
                fd = False
                for k in range(crossover_point, app.tasknum):
                    if temp_l[j] == next_chromosome2[k]:
                        fd = True
                        break
                if not fd:
                    next_chromosome2[delta] = temp_l[j]
                    delta += 1
                    if delta >= crossover_point:
                        break
            if flag:
                if random.randint(0,1) % 2==0:
                    offspring_population.append(prev_chromosome1)
                    # print(list(ii.id for ii in prev_chromosome1))
                else:
                    offspring_population.append(prev_chromosome2)
                    # print(list(ii.id for ii in prev_chromosome2))
            else:
                if random.randint(0,1) % 2==0:
                    offspring_population.append(next_chromosome1)
                    # print(list(ii.id for ii in next_chromosome1))
                else:
                    offspring_population.append(next_chromosome2)
                    # print(list(ii.id for ii in next_chromosome2))
            flag=not flag
        # offspring_population=self.create_population(app,offspring_population)
        return offspring_population

    def mutate(self,app,pop_size, population,MutationRate):
        newpopulation=[]
        for p in population:
            if random.random()<MutationRate:
                while True:
                    pos=random.randint(0,app.tasknum-1)
                    taskid=p[pos]
                    FirstSUC=app.tasknum-1
                    flag=True
                    if taskid.successors:
                        for i in range(pos+1,app.tasknum):
                            for j in taskid.successors:
                                if j==p[i]:
                                    FirstSUC=i
                                    flag=False
                                    break
                            if not flag:
                                break
                    if FirstSUC - pos < 2:
                        continue

                    k=random.randint(pos+1,FirstSUC)
                    taskk=p[k]
                    fll=True
                    if taskk.predecessors:
                        for i in range(pos,k):
                            for j in taskk.predecessors:
                                if j==p[i]:
                                    fll=False
                                    break
                            if not fll:
                                break
                    if fll:
                        break
                    else:
                        continue
                p[pos],p[k]=p[k],p[pos]
                newpopulation.append(p)
            else:
                newpopulation.append(p)
        return newpopulation
        pass

