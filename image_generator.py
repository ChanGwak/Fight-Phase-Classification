# Convert log(.ulg) file to image
import os
from pyulog import ULog
class Flight_data:
    def __init__(self, file_name):
        path = os.getcwd()
        self.file_path = path+'\\Log\\'
        self.file_name = file_name
        self.raw_data = None
        self.data_list = dict()
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

    def pick_data(self, data_name_pair):
        class1 = data_name_pair[0]
        class2 = data_name_pair[1]
        t = self.data_list[class1]['timestamp']
        v = self.data_list[class1][class2]
        return t, v
 
    def interpolation(self, Hz):
        pass