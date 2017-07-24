import pandas as pd
import csv

class HEAD(object):
    def __init__(self, headings_1, headings_2, description, line_num):
        self.head_description = pd.DataFrame(data = [description], columns = headings_1)
        self.data_headings = headings_2
        self.id = int(self.head_description["Head Stack S/N"][0])
        self.line_num = line_num
        self.data = {}
    def add_row(self,row):
        self.head_data = self.head_data.append(pd.DataFrame([row],columns = self.data_headings),
                                               ignore_index = True)
    def deleteData(self):
        self.data = {}
        

def readInitialCSVFile(file_path):
    master = dict()
    with open(file_path,'rb') as csvfile:
        reader = csv.reader(csvfile)
        row = next(reader)
        while row[0] == ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>":
            headings_1 = next(reader)
            description = next(reader)
            row = next(reader)
            headings_2 = next(reader)
            row = next(reader)
            new_head = HEAD(headings_1, headings_2, description, reader.line_num)
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
                    print "reached end of file"
                    break
            master[new_head.id] = new_head
    return master

def readInHEAD(file_path, headings, line_num):
    HEAD_data = pd.DataFrame(columns = headings)
    with open(file_path,'rb') as csvfile:
        reader = csv.reader(csvfile)        
        while True:
            if reader.line_num == line_num:
                break
            try:
                row = next(reader)
            except StopIteration:
                print "ERROR: could not find line"
                break
        while True:
            if len(row) == 0:
                break
            else:
                HEAD_data = HEAD_data.append(pd.DataFrame([row],columns = headings),
                                             ignore_index = True)

if __name__ == '__main__':
    master = readInitialCSVFile("Data-File.csv")
