"""
类别: 基本组件
名称: 处理器类
作者: szf
邮件: zf_sun@vip.hnist.edu.cn
日期: 2022年3月1日
说明: 电压频率组
"""

class VRF(object):

    def __init__(self, voltage=None, frequency=None):
        self.voltage = voltage
        self.frequency = frequency

    def getVoltage(self):
        return self.voltage
    def setVoltage(self, voltage):
        self.voltage=voltage
    def getFrequency(self):
        return self.frequency
    def setFrequency(self, frequency):
        self.frequency=frequency