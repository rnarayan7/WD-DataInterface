import pandas
import os
import matplotlib
from matplotlib.figure import Figure
import csv

class Summary(object):
    def __init__(self, numHEADs, dev, rms):
        self.numHEADs = numHEADs
        self.dev = dev
        self.rms = rms
        
    def PlotDEV(self):
        print "Nothing so far"
        
    def PlotRMS(self):
        print "Nothing so far"

    def PlotMIN(self):
        print "Nothing so far"
        
    def PerformLimitTest(self, index, data):
        print "Nothing so far"