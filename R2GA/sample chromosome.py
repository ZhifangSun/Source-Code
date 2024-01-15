import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from time import *
import tracemalloc

from CONFIG.config import *
from UTIL.logger import Logger
from COMPONENT.application import Application
from service.applicationservice import ApplicationService
from system.computingsystem import ComputingSystem
from UTIL.genericutils import print_list
from SCHEDULER.task.heftscheduler import HeftScheduler
from SCHEDULER.task.geneticscheduler import GeneticScheduler
from SCHEDULER.task.Evolutionscheduler import EvolutionScheduler
from SCHEDULER.task.wolfscheduler import wolfScheduler
from datetime import datetime

processor_number = 3
# Computing system initialization
ComputingSystem.init(processor_number)
# Generating Applications
appA = Application("A")
appB = Application("B")
appC = Application("C")
appD = Application("D")

'''HEFT'''
computation_time_matrix = [
    [11.00, 13.00, 9.00], [10.00, 15.00, 11.00], [9.00, 12.00, 14.00],
    [11.00, 16.00, 10.00], [15.00, 11.00, 19.00], [12.00, 9.00, 5.00],
    [10.00, 14.00, 13.00], [11.00, 15.00, 10.00]
]
computation_cost_matrix = [
    [0.00, 0.00, 0.00], [0.00, 0.00, 0.00], [0.00, 0.00, 0.00],
    [0.00, 0.00, 0.00], [0.00, 0.00, 0.00], [0.00, 0.00, 0.00],
    [0.00, 0.00, 0.00], [0.00, 0.00, 0.00],
]
communication_time_matrix = [
    [INF, 11.00, 17.00, 14.00, 11.00, INF, INF, INF],
    [INF, INF, INF, INF, INF, 13.00, INF, INF],
    [INF, INF, INF, INF, INF, 10.00, INF, INF],
    [INF, INF, INF, INF, INF, 19.00, 13.00, INF],
    [INF, INF, INF, INF, INF, INF, 27.00, INF],
    [INF, INF, INF, INF, INF, INF, INF, 21.00],
    [INF, INF, INF, INF, INF, INF, INF, 13.00],
    [INF, INF, INF, INF, INF, INF, INF, INF]
]
task_number = 8
# Initializing Applications
ApplicationService.init_application(appA, task_number, computation_time_matrix, computation_cost_matrix,
                                    communication_time_matrix)

chromosome=[[0.32,0.67,0.51,0.98,0.24,0.76,0.43,0.35,0.55,0.2,0.11,0.86,0.19,0.46,0.91,0.63]]
genetic = GeneticScheduler("Genetic")  #R2GA
pop ,lists= genetic.create_population(appA,chromosome)
print(lists)
elite_sequence=pop[0]
complete_time={}
for i in elite_sequence.tsk_sequence:
    start_time = lists[0].list[i].running_span.start_time
    finish_time = lists[0].list[i].running_span.finish_time
    span = lists[0].list[i].running_span.span
    id = (elite_sequence.tsk_sequence[elite_sequence.tsk_sequence.index(i)].id, elite_sequence.prossor_sequence[elite_sequence.tsk_sequence.index(i)].id)
    complete_time[id] = (start_time, finish_time, span)
print(complete_time)

colors = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7}
e=255
color = [(144/e,201/e,231/e), (33/e,158/e,188/e), (19/e,103/e,131/e),(21/e,151/e,165/e),(254/e,183/e,5/e),(243/e,162/e,97/e),(250/e,134/e,0/e),(233/e,196/e,107/e)]
for k, v in complete_time.items():
    plt.barh(y=k[1], width=v[2], left=v[0], edgecolor="black", color=color[colors[k[0]]])
    plt.text(v[0]+0.2, k[1], 't'+str(k[0]-1),fontsize=15,	verticalalignment="center")
    # plt.text(v[0] + 0.2, 2 * k[2] - 0.2, str(v[0]) + " " + str(v[1]), fontdict=fontdict_time)

my_y_ticks = np.arange(1, processor_number+1, 1)  # There are 13 points in the original data, so this is a setup that starts at 0 and has an interval of 1.

plt.yticks(my_y_ticks)
plt.title("Gantt chart")
plt.xlabel("makespan")
plt.ylabel("processor")
plt.vlines(elite_sequence.makespan,0,processor_number+1, colors='black',label="makespan="+str(int(elite_sequence.makespan)))
plt.legend(bbox_to_anchor=(0.68, 1.01), loc=3, borderaxespad=0)
plt.savefig("C:\\Users\\85184\\Desktop\\Ganttecs.pdf",format='pdf')
plt.show()