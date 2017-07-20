import pandas as pd
import csv

master = dict()

class HEAD(object):
    def __init__(self, headings_1, headings_2, description):
        self.head_description = pd.DataFrame(data = [description], columns = headings_1)
        self.head_data = pd.DataFrame(columns = headings_2)
    def add_row(self,row):
        self.head_data.append(pd.Series([row]), ignore_index = True)


with open('Data-file.csv','rb') as csvfile:
    reader = csv.reader(csvfile)
    first = next(reader)    
    if first[0] == ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>":
        headings_1 = next(reader)
        description = next(reader)
        placeholder = next(reader)
        headings_2 = next(reader)
        new_head = HEAD(headings_1, headings_2, description)
        row = next(reader)
        while len(row) != 0:
            new_head.add_row(row)
            row = next(reader)