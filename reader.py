import pandas as pd
import matplotlib.pyplot as plt
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

#if __name__ == '__main__':
    #master = readInitialCSVFile("Data-File.csv")
