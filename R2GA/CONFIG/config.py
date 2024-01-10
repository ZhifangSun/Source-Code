#!/usr/bin/env python3
# *-* coding:utf8 *-*

"""
类别: 配置文件
名称: 全局配置文件
作者: strong
邮件: jqjiang@hnist.edu.cn
日期: 2020年3月23日
说明: 对本工程中常用的参数进行集中管理的文件
"""

PRECISION = 1  # 数值精度

ALPHA = 0.9  # 权值1

BETA = 1.0 - ALPHA  # 权值2

INF = float("inf")  # 浮点数正无穷大

F = False

T = True

SHOW_ORIGINAL_SCHEDULING_LIST = True  # 是否打印原始调度序列

SHOW_OPTIMIZED_SCHEDULING_LIST = False  # 是否打印优化调度序列
