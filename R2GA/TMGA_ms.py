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
from UTIL.genericutils import readfile
from SCHEDULER.task.heftscheduler import HeftScheduler
from SCHEDULER.task.geneticscheduler import GeneticScheduler
from SCHEDULER.task.HGAscheduler import HGAScheduler
from SCHEDULER.task.NGAscheduler import NGAScheduler
from SCHEDULER.task.LWSGAscheduler import LWSGAScheduler
from SCHEDULER.task.Evolutionscheduler import EvolutionScheduler
from SCHEDULER.task.wolfscheduler import wolfScheduler
from SCHEDULER.task.TMGA import TMGAScheduler
from datetime import datetime


def main():
    # bandwidth=20;processing capacity=[1,1,2,2,3,3]
    processor_number = 6
    # Computing system initialization
    ComputingSystem.init(processor_number)
    outfilename='Appendix 3.txt'
    filename=["Epigenomics_24_0.xml","Epigenomics_100_0.xml","Epigenomics_997_0.xml","Ligo_30_0.xml","Ligo_100_0.xml","Ligo_1000_0.xml","Montage_25_0.xml","Montage_100_0.xml","Montage_1000_0.xml"]
    file_ms = {"Epigenomics_24_0.xml":2487.797, "Epigenomics_100_0.xml":45547.45, "Epigenomics_997_0.xml":581567.257, "Ligo_30_0.xml":777.237,
                "Ligo_100_0.xml":2357.118, "Ligo_1000_0.xml":71771.596, "Montage_25_0.xml":39.781, "Montage_100_0.xml":150.665, "Montage_1000_0.xml":4972.339}

    for i in filename:
        targetms=file_ms[i]
        output_path = outfilename
        with open(output_path, 'a', encoding='utf-8') as file1:
            print(i, file=file1)
        print(i)
        dex1 = i.index("_")
        dex2 = i.index("_", dex1 + 1)
        sign=int(i[dex1 + 1:dex2])
        computation_time_matrix,communication_time_matrix=readfile(i)
        # for i in computation_time_matrix:
        #     print(i)
        # for i in communication_time_matrix:
        #     print(i)
        # Task execution time matrix
        computation_cost_matrix = [
            [14.00, 9.00, 16.00], [19.00, 13.00, 18.00], [19.00, 13.00, 11.00],
            [13.00, 17.00, 8.00], [12.00, 10.00, 13.00], [13.00, 9.00, 16.00],
            [15.00, 7.00, 11.00], [14.00, 11.00, 5.00], [18.00, 20.00, 12.00],
            [7.00, 21.00, 16.00]
        ]

        task_number = len(computation_time_matrix)
        # task_number = 32
        # Initializing Applications
        # ApplicationService.init_application(appA, task_number, computation_time_matrix, computation_cost_matrix, communication_time_matrix)
        # ApplicationService.init_application(appB, task_number, computation_time_matrix, computation_cost_matrix, communication_time_matrix)
        # ApplicationService.init_application(appC, task_number, computation_time_matrix, computation_cost_matrix, communication_time_matrix)
        # ApplicationService.init_application(appD, task_number, computation_time_matrix, computation_cost_matrix, communication_time_matrix)


        # for ii in range(10):
        #     begin_time = time()
        #     # Generating Applications
        #     appA = Application("A")
        #     genetic = GeneticScheduler("Genetic")  #R2GA
        #     ApplicationService.init_application(genetic,appA, task_number, computation_time_matrix, computation_cost_matrix,communication_time_matrix)
        #     ga_makespan, ga_cost = genetic.schedule(sign,appA,outfilename,targetms,begin_time)
        #     end_time = time()
        #     run_time = end_time - begin_time
        #     output_path = outfilename
        #     with open(output_path, 'a', encoding='utf-8') as file1:
        #         print(run_time, file=file1)
        #     print(run_time)
        # print()
        #
        # for ii in range(10):
        #     begin_time = time()
        #     appB = Application("B")
        #     HGA = HGAScheduler("HGA")  # HGA
        #     ApplicationService.init_application(HGA,appB, task_number, computation_time_matrix, computation_cost_matrix, communication_time_matrix)
        #     hga_makespan, hga_cost = HGA.schedule(sign,appB,outfilename,targetms,begin_time)
        #     end_time = time()
        #     run_time = end_time - begin_time
        #     output_path = outfilename
        #     with open(output_path, 'a', encoding='utf-8') as file1:
        #         print(run_time, file=file1)
        #     print(run_time)
        # print()
        #
        # for ii in range(10):
        #     begin_time = time()
        #     appC = Application("C")
        #     NGA = NGAScheduler("NGA")  # NGA
        #     ApplicationService.init_application(NGA,appC, task_number, computation_time_matrix, computation_cost_matrix, communication_time_matrix)
        #     nga_makespan, nga_cost = NGA.schedule(sign,appC,outfilename,targetms,begin_time)
        #     end_time = time()
        #     run_time = end_time - begin_time
        #     output_path = outfilename
        #     with open(output_path, 'a', encoding='utf-8') as file1:
        #         print(run_time, file=file1)
        #     print(run_time)
        #
        # for ii in range(10):
        #     begin_time = time()
        #     appD = Application("D")
        #     LWSGA = LWSGAScheduler("LWSGA")  # LWSGA
        #     ApplicationService.init_application(LWSGA,appD, task_number, computation_time_matrix, computation_cost_matrix, communication_time_matrix)
        #     lwsga_makespan, lwsga_cost = LWSGA.schedule(sign,appD,outfilename,targetms,begin_time)
        #     end_time = time()
        #     run_time = end_time - begin_time
        #     output_path = outfilename
        #     with open(output_path, 'a', encoding='utf-8') as file1:
        #         print(run_time, file=file1)
        #     print(run_time)
        # print()
        #
        # for ii in range(10):
        #     begin_time = time()
        #     appE = Application("E")
        #     evolution=EvolutionScheduler("Evolution")  #DE
        #     ApplicationService.init_application(evolution,appE, task_number, computation_time_matrix, computation_cost_matrix, communication_time_matrix)
        #     de_makespan = evolution.schedule(appE,outfilename,targetms,begin_time)
        #     end_time = time()
        #     run_time = end_time - begin_time
        #     output_path = outfilename
        #     with open(output_path, 'a', encoding='utf-8') as file1:
        #         print(run_time, file=file1)
        #     print(run_time)
        # print()
        #
        # for ii in range(10):
        #     begin_time = time()
        #     appF = Application("F")
        #     wolf = wolfScheduler("wolf")  #GWO
        #     ApplicationService.init_application(wolf,appF, task_number, computation_time_matrix, computation_cost_matrix, communication_time_matrix)
        #     GWO_makespan= wolf.schedule(appF,outfilename,targetms,begin_time)
        #     end_time = time()
        #     run_time = end_time - begin_time
        #     output_path = outfilename
        #     with open(output_path, 'a', encoding='utf-8') as file1:
        #         print(run_time, file=file1)
        #     print(run_time)
        # print()

        for ii in range(10):
            begin_time = time()
            appG = Application("G")
            TMGA = TMGAScheduler("TMGA")  # TMGA
            ApplicationService.init_application(TMGA, appG, task_number, computation_time_matrix,
                                                computation_cost_matrix,
                                                communication_time_matrix)
            TMGA_makespan = TMGA.schedule(1000,appG, outfilename, targetms, begin_time)
            end_time = time()
            run_time = end_time - begin_time
            output_path = outfilename
            with open(output_path, 'a', encoding='utf-8') as file1:
                print(run_time, file=file1)
            print(run_time)
        with open(output_path, 'a', encoding='utf-8') as file1:
            print(file=file1)
        print()
        print()



if __name__ == '__main__':
    main()
