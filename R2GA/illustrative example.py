#!/usr/bin/env python3
# *-* coding:utf8 *-*

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
from SCHEDULER.task.HGAscheduler import HGAScheduler
from SCHEDULER.task.NGAscheduler import NGAScheduler
from SCHEDULER.task.LWSGAscheduler import LWSGAScheduler
from SCHEDULER.task.Evolutionscheduler import EvolutionScheduler
from SCHEDULER.task.wolfscheduler import wolfScheduler
from datetime import datetime


def main():
    processor_number = 3
    # Computing system initialization
    ComputingSystem.init(processor_number)
    # Generating Applications
    appA = Application("A")
    appB = Application("B")
    appC = Application("C")
    appD = Application("D")
    appE = Application("E")
    appF = Application("F")
    appG = Application("G")

    # Task execution time matrix
    computation_time_matrix = [
        [11.00, 13.00, 9.00], [10.00, 15.00, 11.00], [9.00, 12.00, 14.00],
        [11.00, 16.00, 10.00], [15.00, 11.00, 19.00], [12.00, 9.00, 5.00],
        [10.00, 14.00, 13.00], [11.00, 15.00, 10.00]
    ]
    # Task execution cost matrix
    computation_cost_matrix = [
        [14.00, 9.00, 16.00], [19.00, 13.00, 18.00], [19.00, 13.00, 11.00],
        [13.00, 17.00, 8.00], [12.00, 10.00, 13.00], [13.00, 9.00, 16.00],
        [15.00, 7.00, 11.00], [14.00, 11.00, 5.00], [18.00, 20.00, 12.00],
        [7.00, 21.00, 16.00]
    ]
    # Task communication time matrix
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
    # task_number = 10
    task_number = 8
    # Initializing Applications
    # ApplicationService.init_application(appA, task_number, computation_time_matrix, computation_cost_matrix, communication_time_matrix)
    # ApplicationService.init_application(appB, task_number, computation_time_matrix, computation_cost_matrix, communication_time_matrix)
    # ApplicationService.init_application(appC, task_number, computation_time_matrix, computation_cost_matrix, communication_time_matrix)
    # ApplicationService.init_application(appD, task_number, computation_time_matrix, computation_cost_matrix, communication_time_matrix)

    outfilename='illustrative example'
    begin_time = time()
    tracemalloc.start()
    heft = HeftScheduler("HEFT")
    ApplicationService.init_application(heft,appA, task_number, computation_time_matrix, computation_cost_matrix,
                                        communication_time_matrix)
    tasklist,prolist = heft.schedule(appA)  # HEFT
    print(tasklist)
    print(prolist)
    end_time = time()
    run_time = end_time - begin_time
    print(run_time)

    begin_time = time()
    genetic = GeneticScheduler("Genetic")  #R2GA
    ApplicationService.init_application(genetic, appB, task_number, computation_time_matrix, computation_cost_matrix,
                                        communication_time_matrix)
    ga_makespan, ga_cost = genetic.schedule(8,appB,outfilename,0,0)
    end_time = time()
    run_time = end_time - begin_time
    print(run_time)

    begin_time = time()
    evolution=EvolutionScheduler("Evolution")  #DE
    ApplicationService.init_application(evolution, appC, task_number, computation_time_matrix, computation_cost_matrix,
                                        communication_time_matrix)
    de_makespan = evolution.schedule(appC,outfilename,0,0)
    end_time = time()
    run_time = end_time - begin_time
    print(run_time)

    begin_time = time()
    wolf = wolfScheduler("wolf")  # GWO
    ApplicationService.init_application(wolf, appD, task_number, computation_time_matrix, computation_cost_matrix,
                                        communication_time_matrix)
    GWO_makespan = wolf.schedule(appD,outfilename,0,0)
    end_time = time()
    run_time = end_time - begin_time
    print(run_time)

    begin_time = time()
    HGA = HGAScheduler("HGA")  # HGA
    ApplicationService.init_application(HGA, appE, task_number, computation_time_matrix, computation_cost_matrix,
                                        communication_time_matrix)
    hga_makespan, hga_cost = HGA.schedule(1000,appE,outfilename,0,0)
    end_time = time()
    run_time = end_time - begin_time
    print(run_time)

    begin_time = time()
    NGA = NGAScheduler("NGA")  # NGA
    ApplicationService.init_application(NGA, appF, task_number, computation_time_matrix, computation_cost_matrix,
                                        communication_time_matrix)
    nga_makespan, nga_cost = NGA.schedule(1000,appF,outfilename,0,0)
    end_time = time()
    run_time = end_time - begin_time
    print(run_time)

    begin_time = time()
    LWSGA = LWSGAScheduler("LWSGA")  # LWSGA
    ApplicationService.init_application(LWSGA, appG, task_number, computation_time_matrix, computation_cost_matrix,
                                        communication_time_matrix)
    lwsga_makespan, lwsga_cost = LWSGA.schedule(1000,appG,outfilename,0,0)
    end_time = time()
    run_time = end_time - begin_time
    print(run_time)




if __name__ == '__main__':
    main()
