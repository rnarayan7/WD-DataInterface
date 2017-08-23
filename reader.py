import pandas as pd
from matplotlib.figure import Figure
import csv

class HEAD(object):
    def __init__(self, info_headings, info, data_headings, data_line1, line_num):
        self.info_headings = info_headings
        self.info = info
        self.data_headings = data_headings
        self.serial_num = self.info[self.info_headings.index("Disk Pack S/N")]
        self.id = int(data_line1[self.data_headings.index("Head #")])
        self.line_num = line_num
        self.data = None
    def DeleteData(self):
        self.data = None
    def PlotGraph(self):
        if(self.data is None):
            raise ValueError("data frame empty")
            return
        figure = Figure(figsize = (8.25,6))
        plt = figure.add_axes([0.1,0.1,0.8,0.8])
        plt.plot(self.data["TS_TFCSetup_TD_TFC_Power (mW)"], self.data["TS_TFCSetup_AE_Sensor_DEV"],'blue')
        plt.plot(self.data["TS_TFCSetup_TD_TFC_Power (mW)"], self.data["TS_TFCSetup_AE_Sensor_NMC"],'purple')
        plt.plot(self.data["TS_TFCSetup_TD_TFC_Power (mW)"], self.data["TS_TFCSetup_AE_Sensor_RMS"],'red')
        plt.set_ylim((0,2))
        plt.set_xlim((0,170))
        plt.legend()
        plt.set_xlabel("TFC Power (mW)")
        plt.set_title(self.serial_num)
        return figure

def ReadInitialCSVFile(file_path):
    master = dict()
    with open(file_path,'rb') as csvfile:
        reader = csv.reader(csvfile)
        row = next(reader)
        while row[0] == ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>":
            info_headings = next(reader)
            info = next(reader)
            row = next(reader)
            data_headings = next(reader)
            data_line1 = next(reader)
            new_head = HEAD(info_headings, info, data_headings, data_line1, reader.line_num)
            while len(row) != 0:
                row = next(reader)
            while True:
                if len(row) == 1:
                    if row[0] == ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>":
                        break
                try:
                    row = next(reader)
                except StopIteration:
                    print "Reached end of CSV file"
                    break
            master[new_head.id] = new_head
    return master

def ReadCSVWithLimit(file_path, dev_limit, rms_limit):
    dev = dict()
    rms = dict()
    with open(file_path,'rb') as csvfile:
        reader = csv.reader(csvfile)
        row = next(reader)
        while row[0] == ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>":
            row = next(reader)
            row = next(reader)
            id = int(row[6])
            row = next(reader)
            row = next(reader)
            row = next(reader)
            dev_value = None
            rms_value = None
            while len(row) != 0:
                if dev_value is None:
                    if float(row[11]) > dev_limit: # Compares DEV value at current point
                        dev_value = row[50] # Stores TFC Power value at point where limit is eclipsed
                if rms_value is None:
                    if float(row[17]) > rms_limit: # Compares RMS value at current point
                        rms_value = row[50] # Stores TFC Power value at point where limit is eclipsed
                row = next(reader)
            while True:
                if len(row) == 1:
                    if row[0] == ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>":
                        break
                try:
                    row = next(reader)
                except StopIteration:
                    print "Reached end of CSV file -- Limit test: DEV = " + str(dev_limit) + " | RMS = " + str(rms_limit)
                    break
            dev[id] = dev_value
            rms[id] = rms_value
    return [dev, rms]

def ReadInHEADData(file_path, headings, line_num):
    HEAD_data = pd.DataFrame(columns = headings)
    with open(file_path,'rb') as csvfile:
        reader = csv.reader(csvfile)    
        while reader.line_num != line_num:
            try:
                next(reader)
            except StopIteration:
                print "ERROR: could not find line"
                break
        row = next(reader)
        while len(row) != 0:
            HEAD_data = HEAD_data.append(pd.DataFrame([row],columns = headings),
                                             ignore_index = True)
            row = next(reader)
        print "Dimensions of data table:"
        print HEAD_data.shape
    return HEAD_data
