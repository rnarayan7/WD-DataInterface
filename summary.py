import matplotlib
import numpy as np
from matplotlib.figure import Figure
from matplotlib.axes import Axes

class Summary(object):
    def __init__(self, numHEADs, dev, rms):
        self.numHEADs = numHEADs
        self.dev = dev
        self.rms = rms
        self.min = {}
        for index in self.dev:
            if self.dev[index] is None:
                self.min[index] = self.rms[index]
            elif self.rms[index] is None:
                self.min[index] = self.dev[index]
            else:
                self.min[index] = min(self.dev[index],self.rms[index])
    
    def PlotSummaryGraphs(self):
        # Create full plot
        figure = Figure(figsize = (4.2,6.5))
        
        # Create DEV plot
        devPlot = figure.add_subplot(311)
        devFiltered = dict((k,v) for k,v in self.dev.iteritems() if v is not None)            
        devPlot.hist(np.asarray(devFiltered.values(), dtype = float), bins = 100)                
        self.devPercentage = float(len(devFiltered)) / float(len(self.dev)) * 100
        devPlot.set_title("DEV -- percentage triggered: " + str("%.2f" % self.devPercentage) + "%")
        
        # Create RMS plot
        rmsPlot = figure.add_subplot(312)
        rmsFiltered = dict((k,v) for k,v in self.rms.iteritems() if v is not None)
        rmsPlot.hist(np.asarray(rmsFiltered.values(), dtype = float), bins = 100)
        self.rmsPercentage = float(len(rmsFiltered)) / float(len(self.rms)) * 100
        rmsPlot.set_title("RMS -- percentage triggered: " + str("%.2f" % self.rmsPercentage) + "%")
        
        # Create RMS plot
        minPlot = figure.add_subplot(313)
        minFiltered = dict((k,v) for k,v in self.min.iteritems() if v is not None)
        minPlot.hist(np.asarray(minFiltered.values(), dtype = float), bins = 100)
        self.minPercentage = float(len(minFiltered)) / float(len(self.min)) * 100
        minPlot.set_title("MIN -- percentage triggered: " + str("%.2f" % self.minPercentage) + "%")
        
        # Format and return full plot
        figure.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.8)
        self.figure = figure
        return self.figure