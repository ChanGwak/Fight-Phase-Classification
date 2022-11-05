# Convert log(.ulg) file to image
import os
import csv
from math import nan
import numpy as np
from scipy import interpolate
from pyulog import ULog
class Flight_data:
    def __init__(self, file_name):
        path = os.getcwd()
        self.file_path = path+'\\Log\\'
        self.file_name = file_name
        self.raw_data = None
        self.data_list = dict()
        self.data = dict()
        self.load_raw_data()
    
    def load_raw_data(self):
        if ".ulg:" not in self.file_name:
            self.file_name = self.file_name+".ulg"

        self.raw_data = ULog(self.file_path+self.file_name).data_list

        for i in self.raw_data:
            name = i.name
            n = 1
            while name in self.data_list:
                n = n+1
                name = i.name + str(n)
            self.data_list[name] = i.data

    def pick_data(self, data_Norm):
        f = open('.\Log\\PX4_log_define.csv', 'r', encoding='utf-8')
        rdr = csv.reader(f)
        data_map = dict()
        for line in rdr:
            if 'Norm' in line:continue
            data_map[line[0]] = [str(line[1]), str(line[2])]
        for i in data_Norm:
            if i not in data_map:
                print("Wrong parameter")
                continue
            px4_name = data_map[i][0]
            px4_key = data_map[i][1]
            self.data[i] = [list(self.data_list[px4_name]['timestamp']),list(self.data_list[px4_name][px4_key])]
 
    def interpolation(self, Hz):
        step = int(1000000/Hz)
        if len(self.data) == 0:
            print('need to pick_data')
            return
        min_list = []
        max_list = []
        for i in self.data:
            min_list.append(self.data[i][0][0])
            max_list.append(self.data[i][0][-1])

        ip_start_time = int(np.ceil(max(min_list)/step)*step)
        ip_end_time = int(np.trunc(min(max_list)/step)*step)
        new_time = Linspace(ip_start_time, ip_end_time, step)

        fill_time = Linspace(0, ip_start_time, step)
        fill_data = []
        for i in range(len(fill_time)):
            fill_data.append(nan)

        for i in self.data:
            oldtime = self.data[i][0]
            olddata = self.data[i][1]
            f_lin = interpolate.interp1d(oldtime, olddata, kind='linear')
            new_data = f_lin(new_time)
            self.data[i]=[fill_time+list(new_time), fill_data+list(new_data)]

def Linspace(start, end, step):
    result = []
    l = int((end-start)/step)
    for i in range(l):
        data = start + i*step
        result.append(data)

    return result

