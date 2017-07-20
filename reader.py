import pandas as pd
import csv

master = dict()

class HEAD(object):
    def __init__(self, headings_1, headings_2, description):
        self.head_description = pd.DataFrame(data = [description], columns = headings_1)
        self.head_data = pd.DataFrame(columns = headings_2)
        self.data_headings = headings_2
        self.id = self.head_description["Head Stack S/N"][0]
    def add_row(self,row):
        self.head_data = self.head_data.append(pd.DataFrame([row],columns = self.data_headings),
                                               ignore_index = True)

if __name__ == '__main__':
    with open('Data-file.csv','rb') as csvfile:
        reader = csv.reader(csvfile)
        row = next(reader)
        while row[0] == ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>":
            headings_1 = next(reader)
            description = next(reader)
            row = next(reader)
            headings_2 = next(reader)
            new_head = HEAD(headings_1, headings_2, description)
            row = next(reader)
            while len(row) != 0:
                new_head.add_row(row)
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
