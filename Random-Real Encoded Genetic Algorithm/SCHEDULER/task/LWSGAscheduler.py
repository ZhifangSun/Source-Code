#!/usr/bin/env python3
# *-* coding:utf8 *-*

"""
类别: 调度器
名称: HGA算法调度器 -- 针对任务的调度
作者: 孙质方
邮件: zf_sun@vip.hnist.edu.cn
日期: 2022年5月11日
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
import random
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


class LWSGAScheduler(Scheduler):

    # sys.stdout = Logger('./result/result_%d.html' % (random.randint(1000, 9999)))
    sys.stdout = Logger('D:/pycpp/GABUDGET/result/result_task.html')

    def schedule(self, sign,app,outfilename,target,st):
        output_path = outfilename
        ComputingSystem.reset(app)  # 重置计算系统. !!!VERY IMPORTANT!!!
        pop_size = 500
        CrossoverRate = 0.7
        population = self.init_population(app, pop_size)
        k = 0
        best_ans=[]
        TaskdexOfLevel =[0]
        for i in app.task_groups_from_the_top.values():
            TaskdexOfLevel.append(TaskdexOfLevel[i.group_id]+len(i.tasks))
        while k < 300:
            half_population = []
            half_population.extend(self.select(pop_size,population))#每次选择种群里适应度值靠前的精英种群
            crossover_chromosomes = self.crossover(app,pop_size,TaskdexOfLevel,CrossoverRate,half_population)#前后交叉
            mutation_chromosomes = self.mutate(app,pop_size,TaskdexOfLevel,crossover_chromosomes)#个体变异
            population+=self.create_population(app,mutation_chromosomes)
            population.sort(key=lambda seq: seq.makespan)
            population=population[:len(population)//2]
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
        if sign<=10:
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
        processor_set = ComputingSystem.processors  # 处理器
        chromosomes = []
        tasks = app.tasks
        app.tasks.sort(key=lambda seq: seq.rank_up_value,reverse=True)
        for i in range(0, pop_size):
            LevelIdOfTask=[]
            for j in range(len(app.task_groups_from_the_top)):
                temp=app.task_groups_from_the_top[j].tasks.copy()
                LevelIdOfTask.append(temp)
            # print(LevelIdOfTask)
            chromosome = []
            level=0
            for j in range(0, app.tasknum):
                randtask=LevelIdOfTask[level][random.randint(0, len(LevelIdOfTask[level]) - 1)]
                chromosome.append(randtask)
                LevelIdOfTask[level].remove(randtask)
                if not LevelIdOfTask[level]:
                    level+=1
            for j in range(0, app.tasknum):
                chromosome.append(processor_set[random.randint(0,len(processor_set)-1)])
            chromosomes.append(chromosome)

        population = self.create_population(app, chromosomes)#1000*len(tasks)
        population.sort(key=lambda seq: seq.makespan)
        return population

    def create_population(self, app, chromosomes):
        i = 0
        population = []
        # candidate_tasks = []
        processor_set = ComputingSystem.processors#处理器
        while len(chromosomes) > 0:
            chromosome = chromosomes.pop(0)#取出chromosomes种群中第一个个体
            # print(chromosome)

            tsk_sequence = chromosome[:len(chromosome)//2]

            prossor_sequence = chromosome[len(chromosome)//2:]
            makespan,scheduling_list = self.calculate_response_time_and_cost(app, i, tsk_sequence, prossor_sequence)

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



    def calculate_response_time_and_cost(self, app, counter, task_sequence, processor_sequence):
        ComputingSystem.reset(app)  # 重置计算系统. !!!VERY IMPORTANT!!!

        scheduling_list = self.scheduling_lists.setdefault(counter)#判断字典scheduling_lists里是否有键counter，没有自动添加

        if not scheduling_list:
            scheduling_list = SchedulingList("Scheduling_List_%d" % counter)
            # self.scheduling_lists[counter] = scheduling_list

        for i in range(0, len(task_sequence)):  # 遍历当前消息分组内的所有消息
            task = task_sequence[i]  # 取任务 task
            processor = processor_sequence[i]  # 取任务 task 对应的运行处理器 processor

            start_time = SchedulerUtils.calculate_earliest_start_time(task, processor)  # 当前遍历处理器上最早可用启动时间
            finish_time = start_time + task.processor__computation_time[processor]  # 当前遍历处理器上最早可用结束时间

            running_span = RunningSpan(start_time, finish_time)  # 上述 for 循环结束后, 最合适的处理器已被找出, 此时可以记录下任务的运行时间段
            assignment = Assignment(processor, running_span)  # 同时记录下任务的运行时环境

            task.assignment = assignment  # 设置任务的运行时环境

            task.is_assigned = True  # 标记任务已被分配

            processor.resident_tasks.append(task)  # 将任务添加至处理器的驻留任务集中
            processor.resident_tasks.sort(key=lambda tsk: tsk.assignment.running_span.start_time)  # 对处理器的驻留任务进行排序, 依据任务启动时间升序排列

            scheduling_list.list[task] = assignment  # 将任务与对应运行时环境置于原始调度列表

        makespan = calculate_makespan(scheduling_list)
        # cost = calculate_cost(self.scheduling_lists[counter])
        scheduling_list.makespan = makespan  # 计算原始调度列表的完工时间
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
        return makespan,scheduling_list#, cost

    def select(self,pop_size, population):
        half_population=[]
        for i in range(0,pop_size-1,2):
            p1=random.randint(0,pop_size-1)
            p2 = random.randint(0, pop_size-1)
            while p1==p2:
                p2 = random.randint(0, pop_size-1)
            if p1<p2:
                parent1=p1
            else:
                parent1=p2
            parent2=parent1
            while parent2==parent1:
                p1 = random.randint(0, pop_size-1)
                p2 = random.randint(0, pop_size-1)
                while p1 == p2:
                    p2 = random.randint(0, pop_size-1)
                if p1 < p2:
                    parent2 = p1
                else:
                    parent2 = p2
            half_population.append(population[parent1])
            half_population.append(population[parent2])
        return half_population

    def crossover(self, app,pop_size,TaskdexOfLevel,CrossoverRate, population):
        offspring_population = []
        for i in range(0, pop_size-1, 2):
            if random.random()<CrossoverRate:
                ra=random.randint(0,2)
                if ra==0:
                    temp_l = []
                    RandLevel=random.randint(0,len(TaskdexOfLevel)-2)
                    for j in range(TaskdexOfLevel[RandLevel],TaskdexOfLevel[RandLevel+1]):
                        population[i].chromosome[j], population[i + 1].chromosome[j] = population[i + 1].chromosome[j], population[i].chromosome[j]
                        population[i].chromosome[app.tasknum+j],population[i+1].chromosome[app.tasknum+j]=population[i+1].chromosome[app.tasknum+j],population[i].chromosome[app.tasknum+j]
                    temp_l.append(population[i].chromosome)
                    temp_l.append(population[i+1].chromosome)
                    offspring_population.extend(temp_l)
                elif ra==1:
                    p1=0
                    p2=0
                    temp_l = []
                    for lea in app.task_groups_from_the_top.values():
                        taskid=lea.tasks[random.randint(0,len(lea.tasks)-1)]
                        for j in range(p1,app.tasknum):
                            if population[i].chromosome[j]==taskid:
                                p1=j
                                break
                        for j in range(p2,app.tasknum):
                            if population[i+1].chromosome[j]==taskid:
                                p2=j
                                break
                        population[i].chromosome[p1],population[i].chromosome[p2]=population[i].chromosome[p2],population[i].chromosome[p1]
                        population[i+1].chromosome[p1], population[i+1].chromosome[p2] = population[i+1].chromosome[p2], population[i+1].chromosome[p1]
                    temp_l.append(population[i].chromosome)
                    temp_l.append(population[i+1].chromosome)
                    offspring_population.extend(temp_l)
                else:
                    temp_l = []
                    for lea in app.task_groups_from_the_top.values():
                        taskdex1=population[i].chromosome.index(lea.tasks[random.randint(0,len(lea.tasks)-1)])
                        taskdex2=population[i+1].chromosome.index(lea.tasks[random.randint(0,len(lea.tasks)-1)])
                        population[i].chromosome[app.tasknum+taskdex1], population[i+1].chromosome[app.tasknum+taskdex2] = population[i+1].chromosome[app.tasknum+taskdex2],population[i].chromosome[app.tasknum+taskdex1]
                    temp_l.append(population[i].chromosome)
                    temp_l.append(population[i + 1].chromosome)
                    offspring_population.extend(temp_l)

            else:
                offspring_population.append(population[i].chromosome)
                offspring_population.append(population[i+1].chromosome)

        return offspring_population

    def mutate(self,app,pop_size,TaskdexOfLevel, population):
        offspring_population = []
        processor_set = ComputingSystem.processors  # 处理器
        for i in range(0, pop_size):
            ra = random.randint(0, 2)
            if ra == 0:
                RandLevel = random.randint(0, len(TaskdexOfLevel) - 2)
                LevelIdOfTask = app.task_groups_from_the_top[RandLevel].tasks.copy()
                for j in range(TaskdexOfLevel[RandLevel], TaskdexOfLevel[RandLevel + 1]):
                    population[i][j]=LevelIdOfTask[random.randint(0,len(LevelIdOfTask)-1)]
                    LevelIdOfTask.remove(population[i][j])
                    population[i][app.tasknum+j] =processor_set[random.randint(0,app.processor_number-1)]
                offspring_population.append(population[i])
            elif ra == 1:
                p1 = -1
                p2 = -1
                RandLevel = random.randint(0, len(TaskdexOfLevel) - 2)
                t1=app.task_groups_from_the_top[RandLevel].tasks[random.randint(0, len(app.task_groups_from_the_top[RandLevel].tasks) - 1)]
                t2=app.task_groups_from_the_top[RandLevel].tasks[random.randint(0, len(app.task_groups_from_the_top[RandLevel].tasks) - 1)]
                for j in range(0, app.tasknum):
                    if population[i][j] == t1:
                        p1 = j
                        break
                for j in range(0, app.tasknum):
                    if population[i][j] == t2:
                        p2 = j
                        break
                population[i][p1], population[i][p2] = population[i][p2],population[i][p1]
                offspring_population.append(population[i])
            else:
                gamma = 1 + random.randint(1, app.tasknum // 4)
                while gamma>0:
                    j=random.randint(app.tasknum,app.tasknum*2-1)
                    population[i][j]=processor_set[random.randint(0,app.processor_number-1)]
                    gamma-=1
                offspring_population.append(population[i])
        return offspring_population
        pass
