#!/usr/bin/env python3
# *-* coding:utf8 *-*

"""
类别: 调度器
名称: TMGA算法调度器 -- 针对任务的调度
作者: 孙质方
邮件: zf_sun@vip.hnist.edu.cn
日期: 2023年11月24日
说明:
"""

import sys
import os

import numpy

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
from time import *


class TMGAScheduler(Scheduler):

    # sys.stdout = Logger('./result/result_%d.html' % (random.randint(1000, 9999)))
    # sys.stdout = Logger('E:/pycpp/GABUDGET/result/result_task.html')

    def schedule(self, sign,app,outfilename,target,st):
        output_path = outfilename
        ComputingSystem.reset(app)  # 重置计算系统. !!!VERY IMPORTANT!!!
        processors = ComputingSystem.processors  # 处理器集
        pop_size = 168
        NumOfSubPop=3
        NumOfEliteOfPop=round(500*0.7)
        MutationRate=0.15
        TrmThresholdOfStg1 = round(6 * app.tasknum*len(processors) / pop_size / NumOfSubPop)
        population,stg = self.init_population(app, pop_size, NumOfSubPop)
        k = 0
        Max_iter=300
        best_ans=[]
        BestFitness = population[0][0].makespan
        best_ch = population[0][0]
        for m in range(1,NumOfSubPop):
            if population[m][0].makespan+0.000001<BestFitness:
                BestFitness = population[m][0].makespan
                best_ch = population[m][0]

        NumOfNoImpGen = 1  #the variable for recording the number of consecutive generations that the best chromosome has not been improved -xy6
        while k < Max_iter:
            # print(k)
            population = self.ChrExc(app, population, NumOfSubPop, NumOfEliteOfPop, pop_size)
            for m in range(1, NumOfSubPop):
                if population[m][0].makespan + 0.000001 < BestFitness:
                    BestFitness = population[m][0].makespan
                    best_ch = population[m][0]
            if outfilename == 'Appendix 3.txt':
                if BestFitness <= target:
                    break
                else:
                    Max_iter=Max_iter+0.3  #防止算法在300次迭代之后没有收敛到目标值
            if outfilename == 'Appendix 4.txt':
                T = time()
                if T - st >= target:
                    break
            for m in range(NumOfSubPop):
                new_population = self.select_cr(app,pop_size,population[m],stg)#每次选择种群里适应度值靠前的一半
                mutation_chromosomes = self.mutate(app,pop_size,new_population,stg)#变异
                # mutation_chromosomes = self.mutate(app,crossover_chromosomes)#个体变异
                next_population=self.create_population(app, mutation_chromosomes)
                next_population.sort(key=lambda seq: seq.makespan)

                # if stg==1:
                #     for n in range(pop_size):
                #         self.GnrMS_Evl(mutation_chromosomes[n])
                # else:
                #     for n in range(pop_size):
                #         self.DcdEvl(mutation_chromosomes[n],True)

                # mutation_chromosomes.sort(key=lambda seq: seq.makespan)
                # next_population[0]=self.IFBSI(app,next_population[0].chromosome) # SS improvement
                next_population=self.IFBSI_LBCRI(pop_size,app,next_population) # MS improvemnet

                NxtSubPop=[]
                for n in range(pop_size):
                    if population[m][n] not in NxtSubPop:
                        NxtSubPop.append(population[m][n])
                for n in range(pop_size):
                    if next_population[n] not in NxtSubPop:
                        NxtSubPop.append(next_population[n])
                NxtSubPop.sort(key=lambda seq: seq.makespan)
                NxtSubPop=NxtSubPop[:pop_size]
                population[m]=NxtSubPop
                if population[m][0].makespan+0.000001<BestFitness:
                    BestFitness=population[m][0].makespan
                    best_ch=population[m][0]
                    NumOfNoImpGen=0
            if stg==1 and NumOfNoImpGen==TrmThresholdOfStg1:
                stg=2
            NumOfNoImpGen+=1


            #     population = population[:pop_size//2]
            #     population.extend(self.create_population(app, mutation_chromosomes, NumOfSubPop))
            # for i in range(NumOfSubPop):
            #     population[i].sort(key=lambda seq: seq.makespan)


            # print("<br/>generation = %d, makespan = %.2f, cost = %.2f, time = %s" % (k, population[0].makespan, population[0].cost, datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')))
            k = k + 1
            best_ans.append(best_ch)
            if outfilename == 'Appendix 3.txt':
                if BestFitness <= target:
                    break
                else:
                    Max_iter=Max_iter+0.3  #防止算法在300次迭代之后没有收敛到目标值
            if outfilename == 'Appendix 4.txt':
                T = time()
                if T - st >= target:
                    break

        # print("-" * 100)
        # print("<br/>pop_size = %d<br/>" % pop_size)
        elite_sequence = best_ch
        makespan = elite_sequence.makespan#调度序列完工时间
        cost = elite_sequence.cost#调度序列总成本
        # print(list(ii.id for ii in elite_sequence.tsk_sequence))
        # print(list(ii.id for ii in elite_sequence.prossor_sequence))
        # tradeoff = ALPHA * makespan + BETA * cost
        # output_path = 'out.txt'


        # with open(output_path, 'a', encoding='utf-8') as file1:
        #     print(list(best_ans[i].makespan for i in range(k)), file=file1)
        # print(list(best_ans[i].makespan for i in range(k)))

        # output_path = 'out.txt'
        with open(output_path, 'a', encoding='utf-8') as file1:
            print("The scheduler = %s, makespan = %.2f" % (self.scheduler_name, makespan), file=file1)
        print("The scheduler = %s, makespan = %.2f" % (self.scheduler_name, makespan))

        # print("The scheduler = %s, makespan = %.2f, cost = %.2f, tradeoff = %.2f, slr = %.2f, mcr = %.2f" % (self.scheduler_name,
        #                                                                             makespan, cost, tradeoff,
        #                                                                             makespan / app.cp_min_time,
        #                                                                             cost / app.cp_min_cost))
        if sign <= 100:
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
                plt.text(v[0], k[1], 't' + str(k[0] - 1), fontsize=15, verticalalignment="center")
                # plt.text(v[0] + 0.2, 2 * k[2] - 0.2, str(v[0]) + " " + str(v[1]), fontdict=fontdict_time)

            my_y_ticks = np.arange(1, app.processor_number + 1, 1)  # 原始数据有13个点，故此处为设置从0开始，间隔为1

            plt.yticks(my_y_ticks)
            plt.title("Gantt chart",fontsize=20)
            plt.xlabel("makespan",fontsize=20)
            plt.ylabel("processor",fontsize=20)
            plt.vlines(elite_sequence.makespan, 0, app.processor_number + 1, colors='black',
                       label="makespan=" + str(int(elite_sequence.makespan)))
            plt.legend(bbox_to_anchor=(0.68, 1.01), loc=3, borderaxespad=0)

            plt.gca().margins(x=0)
            plt.gcf().canvas.draw()

            # set size
            maxsize = 70
            m = 0.2
            N = len(complete_time)
            s = maxsize / plt.gcf().dpi * N + 2 * m
            margin = m / plt.gcf().get_size_inches()[0]

            plt.gcf().subplots_adjust(left=margin, right=1. - margin)
            plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])
            plt.savefig("C:\\Users\\85184\\Desktop\\Ganttecs.pdf", format='pdf')
            plt.show()
        return makespan, cost

    def init_population(self, app, pop_size, NumOfSubPop):
        chromosomes = []
        chromosomes1 = []
        chromosomes2 = []
        chromosomes3 = []
        stg=1


        uprank_tasks = app.tasks.copy()
        uprank_tasks.sort(key=lambda seq: seq.rank_up_value, reverse=True)
        # print(list(ii.id for ii in uprank_tasks))
        uprank_tasks_pro=self.Allocation_processor(app,uprank_tasks)
        # print(uprank_tasks_pro)
        chromosome_uprank=uprank_tasks+uprank_tasks_pro
        chromosomes1.append(chromosome_uprank)
        chromosomes2.append(chromosome_uprank)
        chromosomes3.append(chromosome_uprank)
        chromosomes=[chromosomes1, chromosomes2, chromosomes3]

        for mm in range(NumOfSubPop):
            nmb=0
            while len(chromosomes[mm])<pop_size:
                nmb+=1
                if nmb<2*pop_size:
                    TemChrom=self.GnrChr_Lvl_EFT(app)
                    if TemChrom not in chromosomes[mm]:
                        chromosomes[mm].append(TemChrom)
                    else:
                        continue
                elif nmb<4*pop_size:
                    TemChrom=self.GnrChr_TS_EFT(app)
                    if TemChrom not in chromosomes[mm]:
                        chromosomes[mm].append(TemChrom)
                    else:
                        continue
                else:
                    stg=2
                    TemChrom = self.GnrChr_TS_Rnd(app)
                    if TemChrom not in chromosomes[mm]:
                        chromosomes[mm].append(TemChrom)
                    else:
                        continue

        population = []
        for i in range(NumOfSubPop):
            population.append(self.create_population(app, chromosomes[i]))#1000*len(tasks)
        for i in range(NumOfSubPop):
            population[i].sort(key=lambda seq: seq.makespan)
        return population,stg


    def GnrChr_Lvl_EFT(self,app):
        LevelIdOfTask = []
        # print(app.task_groups_from_the_top)
        for j in range(len(app.task_groups_from_the_top)):
            temp = app.task_groups_from_the_top[j].tasks.copy()
            LevelIdOfTask.append(temp)
        # print(LevelIdOfTask)
        chromosome = []
        level = 0
        for j in range(0, app.tasknum):
            randtask = LevelIdOfTask[level][random.randint(0, len(LevelIdOfTask[level]) - 1)]
            chromosome.append(randtask)
            LevelIdOfTask[level].remove(randtask)
            if not LevelIdOfTask[level]:
                level += 1
        GnrMS_Evl = self.Allocation_processor(app, chromosome)
        chromosome.extend(GnrMS_Evl)
        return chromosome

    def GnrChr_TS_EFT(self,app):
        candidate_tasks=[]
        candidate_tasks += app.entry_task  # 添加入口任务
        chromosome = []
        self.reset_tasks(app.tasks)
        for j in range(0, app.tasknum):
            candidate_tasks.sort(key=lambda tsk: tsk.id)
            task = candidate_tasks[random.randint(0, len(candidate_tasks) - 1)]
            # print(task.id,end=' ')
            chromosome.append(task)
            task.is_decoded = True
            candidate_tasks.remove(task)
            for successor in task.successors:
                if self.is_ready(successor):
                    candidate_tasks.append(successor)
        # print(chromosome)
        GnrMS_Evl = self.Allocation_processor(app, chromosome)
        chromosome.extend(GnrMS_Evl)
        return chromosome

    def GnrChr_TS_Rnd(self,app):
        processor_set = ComputingSystem.processors  # 处理器
        candidate_tasks=[]
        candidate_tasks += app.entry_task  # 添加入口任务
        chromosome = []
        self.reset_tasks(app.tasks)
        for j in range(0, app.tasknum):
            candidate_tasks.sort(key=lambda tsk: tsk.id)
            task = candidate_tasks[random.randint(0, len(candidate_tasks) - 1)]
            # print(task.id,end=' ')
            chromosome.append(task)
            task.is_decoded = True
            candidate_tasks.remove(task)
            for successor in task.successors:
                if self.is_ready(successor):
                    candidate_tasks.append(successor)
        for j in range(0, app.tasknum):
            chromosome.append(processor_set[random.randint(0, len(processor_set) - 1)])
        return chromosome

    def create_population(self, app, chromosomes):
        i = 0
        population = []
        # candidate_tasks = []
        processor_set = ComputingSystem.processors  # 处理器
        # print(chromosomes)
        while len(chromosomes) > 0:
            chromosome = chromosomes.pop(0)  # 取出chromosomes种群中第一个个体
            # print(chromosome)

            tsk_sequence = chromosome[:len(chromosome) // 2]

            prossor_sequence = chromosome[len(chromosome) // 2:]
            # for ii in tsk_sequence:
            #     print(ii.id, end=' ')
            # print()
            makespan, scheduling_list = self.calculate_response_time_and_cost(app, i, tsk_sequence, prossor_sequence)

            i = i + 1
            s = Sequence(chromosome, tsk_sequence, prossor_sequence, makespan)
            s.scheduling_list = scheduling_list
            population.append(s)

        return population  # ,self.scheduling_lists

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

    def calculate_response_time_and_cost(self, app, counter, task_sequence, processor_sequence):
        ComputingSystem.reset(app)  # 重置计算系统. !!!VERY IMPORTANT!!!

        scheduling_list = self.scheduling_lists.setdefault(counter)#判断字典scheduling_lists里是否有键counter，没有自动添加

        if not scheduling_list:
            scheduling_list = SchedulingList("Scheduling_List_%d" % counter)
            # self.scheduling_lists[counter] = scheduling_list

        for i in range(0, app.tasknum):  # 遍历当前消息分组内的所有消息
            task = task_sequence[i]  # 取任务 task
            processor = processor_sequence[i]  # 取任务 task 对应的运行处理器 processor
            # print(task, processor)
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

    def select_cr(self,app, pop_size,population,stg):
        flg=True
        newPopulation=[]
        for n in range(0,pop_size,2):
            ind1=random.randint(0,len(population)-1)
            ind2=random.randint(0,len(population)-1)
            while ind2==ind1:
                ind1 = random.randint(0, len(population) - 1)
            chrom1 = population[ind1].chromosome
            chrom2 = population[ind2].chromosome
            if stg==1:
                MOD=random.randint(0,100) % 2
                if MOD==0:
                    scs,chrom1, chrom2=self.Crs_IL(app,chrom1, chrom2, stg)
                    if not scs:
                        chrom1, chrom2=self.Crs_TS(app,chrom1, chrom2, flg, stg)
                        flg = not flg
                else:
                    chrom1, chrom2=self.Crs_TS(app,chrom1, chrom2, flg, stg)
                    flg = not flg
            else:
                MOD=random.randint(0,100) % 3
                if MOD==0:
                    chrom1, chrom2=self.CrsMS_MP(app,chrom1, chrom2)
                if MOD==1:
                    scs, chrom1, chrom2 = self.Crs_IL(app, chrom1, chrom2, stg)
                    if not scs:
                        method=random.randint(0,100) % 2
                        if method==0:
                            chrom1, chrom2=self.Crs_TS(app,chrom1, chrom2, flg, stg)
                            flg = not flg
                        else:
                            chrom1, chrom2=self.CrsMS_MP(app,chrom1, chrom2)
                if MOD==2:
                    chrom1, chrom2=self.Crs_TS(app,chrom1, chrom2, flg, stg)
                    flg = not flg

            newPopulation.append(chrom1)
            newPopulation.append(chrom2)
        #     print('##')
        # print('end')
        return newPopulation

    # def crossover(self, app,pop_size,population):
    #     offspring_population = []
    #     for i in range(0, pop_size//2-1, 2):
    #         prev_chromosome = []
    #         next_chromosome = []
    #         prev_chromosome.extend(population[i].chromosome)
    #         next_chromosome.extend(population[i+1].chromosome)
    #         crossover_point1 = random.randint(1, app.tasknum-2)
    #         crossover_point2 = random.randint(app.tasknum+1, 2*app.tasknum-2)
    #         for j in range(crossover_point1,crossover_point2):
    #             prev_chromosome[j], next_chromosome[j] = next_chromosome[j], prev_chromosome[j]
    #         offspring_population.append(prev_chromosome)
    #         offspring_population.append(next_chromosome)
    #
    #     return offspring_population

    def mutate(self, app,pop_size,new_population,stg):
        if stg==1:
            for n in range(pop_size):
                if random.random()<0.15:
                    MOD=random.randint(0,100)%2
                    if MOD==0:
                        new_population[n]=self.MtnSS_IL(app,new_population[n])
                    else:
                        new_population[n]=self.MtnSS_TS(app,new_population[n])
        else:
            for n in range(pop_size):
                if random.random()<0.15:
                    MOD=random.randint(0,100)%3
                    if MOD==0:
                        new_population[n]=self.MtnSS_IL(app,new_population[n])
                    if MOD==1:
                        new_population[n]=self.MtnSS_TS(app,new_population[n])
                    else:
                        new_population[n]=self.MtnMS_MP(app,new_population[n])
        return new_population
        pass

    def Allocation_processor(self,app,tasks):
        ComputingSystem.reset(app)  # 重置计算系统. !!!VERY IMPORTANT!!!

        processors = ComputingSystem.processors  # 处理器集

        processor = None  # 全局处理器
        temp_task_id = []
        temp_processor = []

        for task in tasks:  # 遍历排序任务集

            earliest_start_time = 0.0  # 初始化全局最早启动时间为0
            earliest_finish_time = float("inf")  # 初始化全局最早结束时间为无穷大

            for p in processors:  # 遍历处理器集

                earliest_start_time_of_this_processor = SchedulerUtils.calculate_earliest_start_time(task,
                                                                                                     p)  # 当前遍历处理器上最早可用启动时间
                earliest_finish_time_of_this_processor = earliest_start_time_of_this_processor + \
                                                         task.processor__computation_time[p]  # 当前遍历处理器上最早可用结束时间

                if earliest_finish_time > earliest_finish_time_of_this_processor:  # 如果全局最早启动时间大于当前遍历处理器上最早可用启动时间, 则
                    earliest_start_time = earliest_start_time_of_this_processor  # 设置全局最早启动时间为当前遍历处理器上最早可用启动时间
                    earliest_finish_time = earliest_finish_time_of_this_processor  # 设置全局最早结束时间为当前遍历处理器上最早可用结束时间
                    processor = p  # 设置全局处理器为当前遍历处理器

            running_span = RunningSpan(earliest_start_time,
                                       earliest_finish_time)  # 上述 for 循环结束后, 最合适的处理器已被找出, 此时可以记录下任务的运行时间段
            assignment = Assignment(processor, running_span)  # 同时记录下任务的运行时环境

            task.assignment = assignment  # 设置任务的运行时环境

            task.is_assigned = True  # 标记任务已被分配

            processor.resident_tasks.append(task)  # 将任务添加至处理器的驻留任务集中
            temp_task_id.append(task.id)
            # print(processor.id)
            temp_processor.append(processor)
            processor.resident_tasks.sort(
                key=lambda tsk: tsk.assignment.running_span.start_time)  # 对处理器的驻留任务进行排序, 依据任务启动时间升序排列
        return temp_processor

    def ChrExc(self, app, population, NumOfSubPop, NumOfEliteOfPop, pop_size):
        EltPop=[]
        for m in range(NumOfSubPop):
            for i in range(len(population[m])):
                if population[m][i] not in EltPop:
                    EltPop.append(population[m][i])
        EltPop.sort(key=lambda seq: seq.makespan)
        EltPop=EltPop[:NumOfEliteOfPop]
        for m in range(NumOfSubPop):
            NewSubPop=[]
            for i in range(len(population[m])):
                if population[m][i] not in NewSubPop:
                    NewSubPop.append(population[m][i])
            for i in range(len(EltPop)):
                if EltPop[i] not in NewSubPop:
                    NewSubPop.append(EltPop[i])
            NewSubPop.sort(key=lambda seq: seq.makespan)
            NewSubPop=NewSubPop[:pop_size]
            population[m].clear()
            population[m].extend(NewSubPop)
        return population

    def Crs_IL(self,app,ch1,ch2,stg):
        scs=True
        IsLvl1=numpy.zeros((len(app.task_groups_from_the_top),2))
        IsLvl2=numpy.zeros((len(app.task_groups_from_the_top),2))
        IsLvl1=self.FndLvl(app,ch1, IsLvl1)
        IsLvl2=self.FndLvl(app,ch2, IsLvl2)
        ComLvl=[]
        for i in range(len(app.task_groups_from_the_top)):
            if IsLvl1[i][0]*IsLvl2[i][0]==1:
                ComLvl.append(i)

        if not ComLvl:
            scs=False
        else:
            RandLevel=ComLvl[random.randint(0,1000)%len(ComLvl)]
            s1=int(IsLvl1[RandLevel][1])
            s2=int(IsLvl2[RandLevel][1])
            for i in range(len(app.task_groups_from_the_top[RandLevel].tasks)):
                ch1[s1],ch2[s2]=ch2[s2],ch1[s1]
                s1+=1
                s2+=1

            if stg==2:
                for i in range(len(app.task_groups_from_the_top[RandLevel].tasks)):
                    TaskIndex = app.task_groups_from_the_top[RandLevel].tasks[i].id-1
                    ch1[TaskIndex+app.tasknum], ch2[TaskIndex+app.tasknum] = ch2[TaskIndex+app.tasknum], ch1[TaskIndex+app.tasknum]
        return scs,ch1,ch2


    def FndLvl(self,app,ch,IsLvl):
        l=0
        cnt=1
        for i in range(1,app.tasknum):
            ff=-1
            for gro in range(len(app.task_groups_from_the_top)):
                for task in app.task_groups_from_the_top[gro].tasks:
                    if ch[i].id==task.id:
                        ff=gro
                        break
                if ff>=0:
                    break
            if l==ff:
                cnt+=1
            else:
                if cnt==len(app.task_groups_from_the_top[l].tasks) and cnt>=2:
                    IsLvl[l][0]=1
                    IsLvl[l][1]=i-cnt
                cnt=1
                l=ff
        # print(l)
        if cnt==len(app.task_groups_from_the_top[l].tasks) and cnt>=2:
            IsLvl[l][0] = 1
            IsLvl[l][1] = app.tasknum - cnt
        return IsLvl

    def Crs_TS(self,app,ch1,ch2,flag,stg):

        # for i in range(len(ch2) // 2):
        #     print(ch1[i].id-1, end=' ')
        # print()
        # for i in range(len(ch2) // 2):
        #     print(ch2[i].id-1, end=' ')
        # print()
        ComputingSystem.reset(app)  # 重置计算系统. !!!VERY IMPORTANT!!!
        processor_set = ComputingSystem.processors#处理器
        gamma=1+random.randint(0,1000)%(app.tasknum-1)
        p1=ch1.copy()
        if flag:##右交叉
            delta=app.tasknum-1
            for i in range(app.tasknum-1,-1,-1):
                fd=False
                for j in range(gamma-1,-1,-1):
                    if ch2[i]==ch1[j]:
                        fd=True
                        break
                if not fd:
                    # print(ch1[delta].id,ch2[i].id)
                    ch1[delta]=ch2[i]
                    ch1[app.tasknum+ch1.index(ch2[i])]=processor_set[(2-stg)*(ch1[app.tasknum+ch1.index(ch2[i])].id-1)+(stg-1)*(ch2[app.tasknum+ch2.index(ch2[i])].id-1)]
                    delta-=1
                    if delta<gamma:
                        break
            delta = app.tasknum - 1
            for i in range(app.tasknum-1,-1,-1):
                fd=False
                for j in range(gamma-1,-1,-1):
                    if ch2[j]==p1[i]:
                        fd=True
                        break
                if not fd:
                    ch2[delta]=p1[i]
                    ch2[app.tasknum+ch2.index(p1[i])]=processor_set[(2-stg)*(ch2[app.tasknum+ch2.index(p1[i])].id-1)+(stg-1)*(p1[app.tasknum+p1.index(p1[i])].id-1)]
                    delta-=1
                    if delta<gamma:
                        break
        else:#左交叉
            delta = 0
            for i in range(app.tasknum):
                fd = False
                for j in range(gamma, app.tasknum):
                    if ch2[i] == ch1[j]:
                        fd = True
                        break
                if not fd:
                    ch1[delta] = ch2[i]
                    ch1[app.tasknum + ch1.index(ch2[i])] = processor_set[
                        (2 - stg) * (ch1[app.tasknum + ch1.index(ch2[i])].id-1) + (stg - 1) * (ch2[
                            app.tasknum + ch2.index(ch2[i])].id-1)]
                    delta += 1
                    if delta >= gamma:
                        break
            delta = 0
            for i in range(app.tasknum):
                fd = False
                for j in range(gamma,app.tasknum):
                    if ch2[j] == p1[i]:
                        fd = True
                        break
                if not fd:
                    ch2[delta] = p1[i]
                    ch2[app.tasknum + ch2.index(p1[i])] = processor_set[
                        (2 - stg) * (ch2[app.tasknum + ch2.index(p1[i])].id-1) + (stg - 1) * (p1[
                            app.tasknum + p1.index(p1[i])].id-1)]
                    delta += 1
                    if delta >= gamma:
                        break
        # print('@@@')
        # for i in range(len(ch2) // 2):
        #     print(ch1[i].id-1, end=' ')
        # print()
        # for i in range(len(ch2) // 2):
        #     print(ch2[i].id-1, end=' ')
        # print()
        # print()
        return ch1,ch2

    def CrsMS_MP(self,app,ch1,ch2):
        for i in range(len(app.task_groups_from_the_top)):
            TaskId=app.task_groups_from_the_top[i].tasks[random.randint(0,1000)%len(app.task_groups_from_the_top[i].tasks)].id-1
            # print(app.tasknum,TaskId)
            ch1[app.tasknum+TaskId],ch2[app.tasknum+TaskId]=ch2[app.tasknum+TaskId],ch1[app.tasknum+TaskId]

        return ch1,ch2

    def MtnSS_IL(self,app,ch):
        IsLvl=numpy.zeros((len(app.task_groups_from_the_top),2))
        IsLvl=self.FndLvl(app,ch,IsLvl)
        AvlLvl=[]
        for i in range(len(app.task_groups_from_the_top)):
            if int(IsLvl[i][0])==1:
                AvlLvl.append(i)
        if not AvlLvl:
            return ch

        RandLevel=AvlLvl[random.randint(1,1000)%len(AvlLvl)]
        s=int(IsLvl[RandLevel][1])
        gamma1=random.randint(0,1000)%len(app.task_groups_from_the_top[RandLevel].tasks)+s
        gamma2 = random.randint(0, 1000) % len(app.task_groups_from_the_top[RandLevel].tasks) + s
        while gamma1==gamma2:
            gamma1 = random.randint(0, 1000) % len(app.task_groups_from_the_top[RandLevel].tasks) + s
        ch[gamma1],ch[gamma2]=ch[gamma2],ch[gamma1]
        return ch

    def MtnSS_TS(self,app,ch):
        pos=random.randint(0,1000)%app.tasknum
        TaskID=ch[pos]
        str=pos-1
        end=pos+1
        while (str>-1 and (ch[str] not in TaskID.predecessors)):
            str-=1
        str+=1
        while (end<app.tasknum and (ch[end] not in TaskID.successors)):
            end+=1
        if end-str<=1:
            return ch

        InsertPoint=random.randint(0,1000)%(end-str)+str
        while InsertPoint==pos:
            InsertPoint=random.randint(0,1000)%(end-str)+str
        if InsertPoint<pos:
            for i in range(pos,InsertPoint-1,-1):
                ch[i]=ch[i-1]
            ch[InsertPoint]=TaskID
        else:
            for i in range(pos,InsertPoint):
                ch[i]=ch[i+1]
            ch[InsertPoint]=TaskID
        return ch

    def MtnMS_MP(self,app,ch):
        processors = ComputingSystem.processors  # 处理器集
        gamma=random.randint(0,1000)%round(app.tasknum/4+1)
        while gamma:
            i=random.randint(0,1000)%app.tasknum
            j=random.randint(0,1000)%len(processors)
            ch[i+app.tasknum]=processors[j]
            gamma-=1
        return ch

    def IFBSI(self,app,ch):
        IsFrw=False
        NewChrom=ch.copy()
        OldChrom = NewChrom.copy()
        ind=self.IndexSort(app, [OldChrom[i].assignment.running_span.finish_time for i in range(len(OldChrom)//2)])
        # print(ind)
        # for i in range(app.tasknum):
        #     NewChrom[app.tasknum - 1 - i] = app.tasks[ind[i]]
        # for ii in NewChrom:
        #     print(ii.id-1, end=' ')
        # print()
        NewChrom=self.create_population(app,[NewChrom])
        # DcdEvl(NewChrom, IsFrw)
        IsFrw = not IsFrw
        while NewChrom.makespan+0.000001< OldChrom.makespan:
            # NewChrom = ch.copy()
            OldChrom = NewChrom.copy()
            ind = self.IndexSort(app, [OldChrom[i].assignment.running_span.finish_time for i in range(len(OldChrom)//2)])
            for i in range(app.tasknum):
                NewChrom[app.tasknum - 1 - i] = app.tasks[ind[i]]
            NewChrom = self.create_population(app, [NewChrom])
            IsFrw = not IsFrw
        if IsFrw:
            ch=OldChrom
        else:
            ch=NewChrom
        return ch

    def IndexSort(self,app, fitness):
        result = fitness.copy()  # Copy fitness values to result list
        ind = [i for i in range(app.tasknum)]  # Initialize the ind list with indices

        # Sort the indices in ind based on corresponding fitness values in result
        ind.sort(key=lambda v: result[v],reverse=True)

        return ind

    def IFBSI_LBCRI(self,pop_size,app,population):
        ComputingSystem.reset(app)  # 重置计算系统. !!!VERY IMPORTANT!!!
        processor_set = ComputingSystem.processors#处理器 = ComputingSystem.processors#处理器
        for i in range(pop_size):
            ft = [0, 0, 0, 0, 0, 0]
            for j in range(app.tasknum):
                ID = population[i].prossor_sequence[j].id - 1
                ans = population[i].scheduling_list.list[population[i].tsk_sequence[j]].running_span.finish_time
                if ft[ID] < ans:
                    ft[ID] = ans
            lb = population[i].makespan - min(ft)
            population[i].lf = lb
            population[i].ft = ft
        # print(len(population))
        population.sort(key=lambda seq: seq.lf)
        for i in range(pop_size // 2, pop_size):
            # print('#####')
            # print(population[i].ft)
            bigprossor = population[i].ft.index(max(population[i].ft))
            # print(bigprossor)
            dex = []
            for j in range(app.tasknum):
                # print(population[i].prossor_sequence[j].id - 1,end='$')
                if population[i].chromosome[j+app.tasknum].id-1 == bigprossor:
                    dex.append(j)
            # print()
            # print(f'~~{dex}')
            # print(population[i].chromosome)
            chro = population[i].chromosome.copy()
            ran = random.randint(0, app.processor_number - 1)
            if ran == bigprossor:
                ran = random.randint(0, app.processor_number - 1)
            chro[dex[random.randint(0, len(dex) - 1)]+app.tasknum] = processor_set[ran]
            new_chr = self.create_population(app, [chro])
            if new_chr[0].makespan < population[i].makespan:
                population[i] = new_chr[0]
        return population