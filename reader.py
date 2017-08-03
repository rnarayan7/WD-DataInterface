import pandas as pd
import matplotlib
from matplotlib.figure import Figure
import csv

class HEAD(object):
    def __init__(self, headings_1, headings_2, description, line_num):
        self.description = description
        self.description_headings = headings_1
        self.data_headings = headings_2
        self.id = int(self.description[6])
        self.serial_num = ""
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
            headings_1 = next(reader)
            description = next(reader)
            row = next(reader)
            headings_2 = next(reader)
            new_head = HEAD(headings_1, headings_2, description, reader.line_num)
            row = next(reader)
            new_head.serial_num = row[4]
            while len(row) != 0:
                #new_head.add_row(row)
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
                        #print "reached dev: " + row[50]
                if rms_value is None:
                    if float(row[17]) > rms_limit: # Compares RMS value at current point
                        rms_value = row[50] # Stores TFC Power value at point where limit is eclipsed
                        #print "reached rms: " + row[50]
                #print "dev: " + str(row[11]) + " rms: " + str(row[17]) + " row[50]: " + str(row[50])
                row = next(reader)
            while True:
                if len(row) == 1:
                    if row[0] == ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>":
                        break
                try:
                    row = next(reader)
                    #break
                except StopIteration:
                    print "Reached end of CSV file -- Limit test: DEV = " + str(dev_limit) + " | RMS = " + str(rms_limit)
                    break
            dev[id] = dev_value
            rms[id] = rms_value
            print "id: " + str(id)
            print "dev_value: " + str(dev_value)
            print "rms_value: " + str(rms_value)
            print ""
    
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
