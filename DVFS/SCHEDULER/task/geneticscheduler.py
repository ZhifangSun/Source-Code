#!/usr/bin/env python3
# *-* coding:utf8 *-*

"""
类别: 调度器
名称: 遗传算法调度器 -- 针对任务的调度
作者: strong
邮件: jqjiang@hnist.edu.cn
日期: 2020年11月22日
说明:2022年5月21日修改(孙质方)
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
from COMPONENT.assignedprocessor import AssignedProcessor
from UTIL.genericutils import *
from UTIL.logger import Logger
from CONFIG.config import *
from itertools import permutations, product
from datetime import datetime
from copy import *
import random
from time import *
import matplotlib.pyplot as plt
import numpy as np


class GeneticScheduler(Scheduler):

    # sys.stdout = Logger('./result/result_%d.html' % (random.randint(1000, 9999)))
    # sys.stdout = Logger('D:/pycpp/GABUDGET/result/result_task.html')

    def schedule(self, sign,app,outfilename,target,st):
        output_path = outfilename
        ComputingSystem.reset(app)  # 重置计算系统. !!!VERY IMPORTANT!!!
        pop_size = 500
        population = self.init_population(app, pop_size)
        k = 0
        best_ans=[]
        s=pop_size//2
        while k < 300:
            half_population = []
            half_population.extend(self.select(pop_size,population,s))#Select the top 50% of the population in terms of fitness values each time
            crossover_chromosomes = self.crossover(app,pop_size,population,s)
            mutation_chromosomes = self.mutate(app,crossover_chromosomes)
            population = population[:s]
            population.extend(self.create_population(app, mutation_chromosomes))
            population.sort(key=lambda seq: seq.tradeoff)
            # print("<br/>generation = %d, makespan = %.2f, cost = %.2f, time = %s" % (k, population[0].makespan, population[0].cost, datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')))

            best_ans.append(population[0])
            if outfilename == 'Appendix 1.txt':
                k = k + 1
            if outfilename=='Appendix 3.txt':
                if population[0].makespan<=target:
                    break
            if outfilename=='Appendix 4.txt':
                T = time()
                if T-st>=target:
                    break

        # print("-" * 100)
        # print("<br/>pop_size = %d<br/>" % pop_size)
        elite_sequence = population[0]
        makespan = elite_sequence.makespan#makespan
        cost = elite_sequence.cost#cost
        # tradeoff = ALPHA * makespan + BETA * cost
        if outfilename == 'Appendix 1.txt':
            with open(output_path, 'a', encoding='utf-8') as file1:
                print(list(best_ans[i].makespan for i in range(k)), file=file1)
            print(list(best_ans[i].makespan for i in range(k)))

        output_path = outfilename
        with open(output_path, 'a', encoding='utf-8') as file1:
            print("The scheduler = %s, makespan = %.2f, allE = %.2f, tradeoff = %.2f" % (self.scheduler_name, makespan, elite_sequence.allE, elite_sequence.tradeoff), file=file1)
        print("The scheduler = %s, makespan = %.2f, allE = %.2f, tradeoff = %.2f" % (self.scheduler_name, makespan, elite_sequence.allE, elite_sequence.tradeoff))

        # print("The scheduler = %s, makespan = %.2f, cost = %.2f, tradeoff = %.2f, slr = %.2f, mcr = %.2f" % (self.scheduler_name,
        #                                                                             makespan, cost, tradeoff,
        #                                                                             makespan / app.cp_min_time,
        #                                                                             cost / app.cp_min_cost))
        # if sign <= 10:
        #     complete_time = {}
        #     lists=elite_sequence.scheduling_list
        #     for i in elite_sequence.tsk_sequence:
        #         start_time = lists.list[i].running_span.start_time
        #         finish_time = lists.list[i].running_span.finish_time
        #         span = lists.list[i].running_span.span
        #         id = (elite_sequence.tsk_sequence[elite_sequence.tsk_sequence.index(i)].id,
        #               elite_sequence.prossor_sequence[elite_sequence.tsk_sequence.index(i)].id)
        #         complete_time[id] = (start_time, finish_time, span)
        #     # print(complete_time)
        #
        #     colors = {}
        #     col=0
        #     for i in range(1,app.tasknum+1):
        #         colors[i]=col
        #         col+=1
        #         if col>7:
        #             col=0
        #     e = 255
        #     color = [(144 / e, 201 / e, 231 / e), (33 / e, 158 / e, 188 / e), (19 / e, 103 / e, 131 / e),
        #              (21 / e, 151 / e, 165 / e), (254 / e, 183 / e, 5 / e), (243 / e, 162 / e, 97 / e),
        #              (250 / e, 134 / e, 0 / e), (233 / e, 196 / e, 107 / e)]
        #     for k, v in complete_time.items():
        #         plt.barh(y=k[1], width=v[2], left=v[0], edgecolor="black", color=color[colors[k[0]]])
        #         plt.text(v[0] + 0.2, k[1], 't' + str(k[0] - 1), fontsize=10, verticalalignment="center")
        #         # plt.text(v[0] + 0.2, 2 * k[2] - 0.2, str(v[0]) + " " + str(v[1]), fontdict=fontdict_time)
        #
        #     my_y_ticks = np.arange(1, app.processor_number + 1, 1)  # 原始数据有13个点，故此处为设置从0开始，间隔为1
        #
        #     plt.yticks(my_y_ticks)
        #     plt.title("Gantt chart")
        #     plt.xlabel("makespan")
        #     plt.ylabel("processor")
        #     plt.vlines(elite_sequence.makespan, 0, app.processor_number + 1, colors='black',
        #                label="makespan=" + str(int(elite_sequence.makespan)))
        #     plt.legend(bbox_to_anchor=(0.68, 1.01), loc=3, borderaxespad=0)
        #
        #     plt.gca().margins(x=0)
        #     plt.gcf().canvas.draw()
        #
        #     # set size
        #     maxsize = 100
        #     m = 0.2
        #     N = len(complete_time)
        #     s = maxsize / plt.gcf().dpi * N + 2 * m
        #     margin = m / plt.gcf().get_size_inches()[0]
        #
        #     plt.gcf().subplots_adjust(left=margin, right=1. - margin)
        #     plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])
        #     # plt.savefig("C:\\Users\\85184\\Desktop\\Ganttecs.pdf", format='pdf')
        #     plt.show()
        return makespan, cost

    def init_population(self, app, pop_size):
        chromosomes = []

        uprank_tasks = app.tasks.copy()
        uprank_tasks.sort(key=lambda seq: seq.rank_up_value, reverse=True)
        # print(list(ii.id for ii in uprank_tasks))
        uprank_tasks_pro=self.Allocation_processor(app,uprank_tasks)
        # print(uprank_tasks_pro)
        candidate_tasks = []
        chromosome1=[]
        chromosome2 = []
        chromosome3=[]
        candidate_tasks += app.entry_task  # 添加入口任务
        self.reset_tasks(app.tasks)
        for j in range(0, app.tasknum):
            candidate_tasks.sort(key=lambda tsk: tsk.id)
            task = uprank_tasks[j]
            tadex=candidate_tasks.index(task)
            l=len(candidate_tasks)
            gene=tadex/l+random.random()/l
            chromosome1.append(gene)
            task.is_decoded = True
            candidate_tasks.remove(task)
            for successor in task.successors:
                if self.is_ready(successor):
                    candidate_tasks.append(successor)
            chromosome2.append((uprank_tasks_pro[j]-1)/app.processor_number+random.random()/app.processor_number)
            chromosome3.append(random.random())
        chromosomes.append(chromosome1+chromosome2+chromosome3)

        # downrank_tasks = app.tasks.copy()
        # downrank_tasks.sort(key=lambda seq: seq.rank_down_value)
        # downrank_tasks_pro=self.Allocation_processor(app,downrank_tasks)
        # candidate_tasks = []
        # chromosome1 = []
        # chromosome2 = []
        # candidate_tasks += app.entry_task  # 添加入口任务
        # self.reset_tasks(app.tasks)
        # for j in range(0, app.tasknum):
        #     candidate_tasks.sort(key=lambda tsk: tsk.id)
        #     task = downrank_tasks[j]
        #     tadex = candidate_tasks.index(task)
        #     l = len(candidate_tasks)
        #     gene = tadex / l + random.random() / l
        #     chromosome1.append(gene)
        #     task.is_decoded = True
        #     candidate_tasks.remove(task)
        #     for successor in task.successors:
        #         if self.is_ready(successor):
        #             candidate_tasks.append(successor)
        #     chromosome2.append(
        #         (downrank_tasks_pro[j] - 1) / app.processor_number + random.random() / app.processor_number)
        # chromosomes.append(chromosome1 + chromosome2)
        #
        # candidate_tasks = []
        # candidate_tasks += app.entry_task  # 添加入口任务
        # udrank_tasks = []
        # self.reset_tasks(app.tasks)
        # for j in range(0, app.tasknum):
        #     candidate_tasks.sort(key=lambda tsk: tsk.rank_sum_value, reverse=True)
        #     task = candidate_tasks[0]
        #     udrank_tasks.append(task)
        #     task.is_decoded = True
        #     candidate_tasks.remove(task)
        #     for successor in task.successors:
        #         if self.is_ready(successor):
        #             candidate_tasks.append(successor)
        # # print(list(idd.id for idd in udrank_tasks))
        # udrank_tasks_pro=self.Allocation_processor(app,udrank_tasks)
        # candidate_tasks = []
        # chromosome1 = []
        # chromosome2 = []
        # candidate_tasks += app.entry_task  # 添加入口任务
        # self.reset_tasks(app.tasks)
        # for j in range(0, app.tasknum):
        #     candidate_tasks.sort(key=lambda tsk: tsk.id)
        #     task = udrank_tasks[j]
        #     tadex = candidate_tasks.index(task)
        #     l = len(candidate_tasks)
        #     gene = tadex / l + random.random() / l
        #     chromosome1.append(gene)
        #     task.is_decoded = True
        #     candidate_tasks.remove(task)
        #     for successor in task.successors:
        #         if self.is_ready(successor):
        #             candidate_tasks.append(successor)
        #     chromosome2.append(
        #         (udrank_tasks_pro[j] - 1) / app.processor_number + random.random() / app.processor_number)
        # chromosomes.append(chromosome1 + chromosome2)




        for i in range(1, pop_size):
            chromosome = []
            for j in range(0, 3 * app.tasknum):#Triple the number of tasks
                chromosome.append(random.random())
            chromosomes.append(chromosome)

        population = self.create_population(app, chromosomes)#1000*len(tasks)
        population.sort(key=lambda seq: seq.tradeoff)
        return population

    def create_population(self, app, chromosomes):
        i = 0
        population = []
        candidate_tasks = []
        processor_set = ComputingSystem.processors#Unit
        vrf_set = ComputingSystem.VRFs[0]#Voltage Frequency
        while chromosomes:    #2 * len(tasks)
            self.reset_tasks(app.tasks)
            candidate_tasks.clear()
            candidate_tasks+=app.entry_task#Adding Entry Tasks
            chromosome = chromosomes.pop(0)#Remove the first individual in the chromosomes population.
            # print(chromosome)

            tsk_sequence = []
            prossor_sequence = []
            vrf_sequence = []
            for j in range(0, app.tasknum):#len(chromosome)//2
                gene = chromosome[j]
                candidate_tasks.sort(key=lambda tsk: tsk.id)
                size = len(candidate_tasks)#Number of tasks with an entry level of 0
                # print(size)
                # scale = 1.0 / size
                # tsk_index = self.get_index(gene, scale, size)#???
                tsk_index=int(gene*size)
                # print(tsk_index)
                task = candidate_tasks[tsk_index]
                task.is_decoded = True
                tsk_sequence.append(task)
                candidate_tasks.remove(task)
                for successor in task.successors:
                    if self.is_ready(successor):
                        candidate_tasks.append(successor)

                prossor_gene = chromosome[app.tasknum+j]
                processor_set.sort(key=lambda prossor: prossor.id)
                # prossor_size = app.processor_number
                # prossor_scale = 1.0 / prossor_size
                # prossor_index = self.get_index(prossor_gene, prossor_scale, prossor_size)
                prossor_index=int(prossor_gene*app.processor_number)
                processor = processor_set[prossor_index]
                prossor_sequence.append(processor)

                vrf_gene = chromosome[2*app.tasknum+j]
                vrf_sequence.append(int(vrf_gene*len(vrf_set)))

            makespan,scheduling_list = self.calculate_response_time_and_cost(app, i, tsk_sequence, prossor_sequence, vrf_sequence)
            # print(scheduling_list.allE)
            # print(prossor_sequence)
            i = i + 1
            s = Sequence(chromosome, tsk_sequence, prossor_sequence, makespan,scheduling_list.allE)
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

    # def get_index(self, gene, scale, size):#gene个体的基因，scale=1/size
    #     l = 0
    #     r = size
    #     mid=(l + r) // 2
    #     while l <= r:
    #         temp = mid * scale
    #         if temp < gene:
    #             l = mid+1
    #         elif temp > gene:
    #             r = mid-1
    #         else:
    #             return mid
    #         mid = (l + r) // 2
    #     return mid
        # i = 1
        # while i <= size:
        #     if i*scale < gene:
        #         i = i + 1
        #     else:
        #         break
        # return i-1

    def calculate_response_time_and_cost(self, app, counter, task_sequence, processor_sequence, vrf_sequence):
        ComputingSystem.reset(app)  # 重置计算系统. !!!VERY IMPORTANT!!!
        processors = ComputingSystem.processors1  # processor set
        vrf_set = ComputingSystem.VRFs[0]#Voltage Frequency

        scheduling_list = self.scheduling_lists.setdefault(counter)#Determine if there is a key counter in the dictionary scheduling_lists and add it automatically if there isn't.

        if not scheduling_list:
            scheduling_list = SchedulingList("Scheduling_List_%d" % counter)
            # self.scheduling_lists[counter] = scheduling_list

        for i in range(0, app.tasknum):  # Iterate through all messages in the current message group
            task = task_sequence[i]  # 取任务 task
            processor = processor_sequence[i]  # Fetch the running processor processor corresponding to the task
            vrf=vrf_set[vrf_sequence[i]]

            start_time = SchedulerUtils.calculate_earliest_start_time(task, processor)  # Earliest available startup time on the current traversal processor
            finish_time = start_time + task.processor__computation_time[processor]  # Earliest available end time on the current traversal processor

            running_span = RunningSpan(start_time, finish_time)  # At the end of the above for loop, the most suitable processor has been found out, then you can record the running span of the task.
            assignment = AssignedProcessor(processor, vrf, running_span)  # Also record the runtime environment of the task
            # assignment = Assignment(processor, running_span)  # Also record the runtime environment of the task

            task.assignment = assignment  # Set the runtime environment of the task

            task.is_assigned = True  # Mark the task as assigned

            processor.resident_tasks.append(task)  # add the task to the processor's resident task set
            processor.resident_tasks.sort(key=lambda tsk: tsk.assignment.running_span.start_time)  # Sort the processor's resident tasks, in ascending order by task start time

            scheduling_list.list[task] = assignment  # Place the task in the original scheduling list with the corresponding runtime environment.

        makespan = calculate_makespan(scheduling_list)
        # cost = calculate_cost(self.scheduling_lists[counter])
        scheduling_list.makespan = makespan  # Calculate the completion time of the original dispatch list
        allE=consumeEnergyInVRF(processors,scheduling_list,makespan)
        scheduling_list.allE=allE
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

    def select(self, pop_size,population,s):
        half_population = population[:s]
        return half_population

    def crossover(self, app,pop_size,population,s):
        offspring_population = []
        for i in range(0, s-1, 2):
            prev_chromosome = []
            next_chromosome = []
            prev_chromosome.extend(population[i].chromosome)
            next_chromosome.extend(population[i+1].chromosome)
            crossover_point1 = random.randint(1, app.tasknum-2)
            crossover_point2 = random.randint(app.tasknum+1, 2*app.tasknum-2)
            crossover_point3 = random.randint(2*app.tasknum+1, 3*app.tasknum-2)
            for j in range(crossover_point1,crossover_point2):
                prev_chromosome[j], next_chromosome[j] = next_chromosome[j], prev_chromosome[j]
            for j in range(crossover_point3,3*app.tasknum):
                prev_chromosome[j], next_chromosome[j] = next_chromosome[j], prev_chromosome[j]
            offspring_population.append(prev_chromosome)
            offspring_population.append(next_chromosome)

        return offspring_population

    def mutate(self, app,population):
        for p in population:
            pos1 = random.randint(0, app.tasknum-1)
            pos2 = random.randint(app.tasknum, 2*app.tasknum-1)
            pos3 = random.randint(2*app.tasknum, 3*app.tasknum-1)
            p[pos1] = random.random()
            p[pos2] = random.random()
            p[pos3] = random.random()
        return population
        pass

    def Allocation_processor(self,app,tasks):
        ComputingSystem.reset(app)  # 重置计算系统. !!!VERY IMPORTANT!!!

        processors = ComputingSystem.processors  # processor set

        processor = None  # global processor
        temp_task_id = []
        temp_processor_id = []

        for task in tasks:  # Iterate through the set of sorting tasks

            earliest_start_time = 0.0  # Initialize the global earliest start time to 0
            earliest_finish_time = float("inf")  # Initialize the global earliest end time to infinity

            for p in processors:  # traverse the set of processors

                earliest_start_time_of_this_processor = SchedulerUtils.calculate_earliest_start_time(task,
                                                                                                     p)  # Earliest available start time of the currently traversed processor
                earliest_finish_time_of_this_processor = earliest_start_time_of_this_processor + \
                                                         task.processor__computation_time[p]  # earliest available finish time of the current traversal processor

                if earliest_finish_time > earliest_finish_time_of_this_processor:  # If the global earliest start time is greater than the earliest available start time on the currently traversed processor, then
                    earliest_start_time = earliest_start_time_of_this_processor  # Set the global earliest start time to the earliest available start time on the current traversal processor.
                    earliest_finish_time = earliest_finish_time_of_this_processor  # Set the global earliest finish time to the earliest available finish time on the current traversal processor
                    processor = p  # Set the global processor to the currently traversed processor

            running_span = RunningSpan(earliest_start_time,
                                       earliest_finish_time)  # At the end of the above for loop, the most suitable processor has been found, and the running span of the task can be recorded at this point.
            assignment = Assignment(processor, running_span)  # Also record the runtime environment of the task
            task.assignment = assignment  # Set the runtime environment of the task

            task.is_assigned = True  # mark the task as assigned

            processor.resident_tasks.append(task)  # add the task to the processor's resident task set
            temp_task_id.append(task.id)
            # print(processor.id)
            temp_processor_id.append(processor.id)
            processor.resident_tasks.sort(
                key=lambda tsk: tsk.assignment.running_span.start_time)  # Sort the processor's resident tasks, in ascending order of task start time
        return temp_processor_id
