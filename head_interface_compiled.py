import csv
import wx
import os
import shutil
import pandas as pd
import numpy as np
import matplotlib
from matplotlib.figure import Figure
import matplotlib.pyplot
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

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
        #for index in self.dev:
            #print "dev: " + str(self.rms[index])
        #for index in self.rms:
            #print "rms: " + str(self.rms[index])

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

# Main window class
class MainWindow(wx.Frame):
    def __init__(self,parent,style,title):
        super(MainWindow, self).__init__(parent, title = title,
            style = style, size = wx.Size(1400,800))
        self.InitUI()
        self.Centre()
        self.Show()
        self.master = {}
        self.currentID = None
        #self.currentFilePath
        #self.listBox
        #self.middlePanel
        #self.graphInfo
        #self.rightPanel
        #self.textEntryDEV
        #self.textEntryRMS
        #self.summaryCanvas

    # Initialize the UI
    def InitUI(self):
        panel = wx.Panel(self)
        mainBox = wx.BoxSizer(wx.HORIZONTAL)
        middleBox = wx.BoxSizer(wx.VERTICAL)
        # Initialize panels
        self.middlePanel = wx.Panel(parent = panel, style = wx.DOUBLE_BORDER)
        self.rightPanel = wx.Panel(parent = panel, style = wx.DOUBLE_BORDER)
        leftPanel = wx.Panel(parent = panel, style = wx.DOUBLE_BORDER)
        # Add components to Main Window BoxSizer
        mainBox.Add(leftPanel, proportion = 1, flag = wx.EXPAND | wx.ALIGN_CENTER | wx.LEFT, border = 10)
        mainBox.Add(self.middlePanel, proportion = 6, flag = wx.EXPAND | wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, border = 5)
        mainBox.Add(self.rightPanel, proportion = 5, flag = wx.EXPAND | wx.ALIGN_CENTER | wx.RIGHT, border = 10)
        panel.SetSizer(mainBox)

        # Create UI of left Panel
        leftBox = wx.BoxSizer(wx.VERTICAL)
        # Create FileDialog button
        openFileDlgBtn = wx.Button(parent = leftPanel, label = "Select a data file")
        openFileDlgBtn.Bind(wx.EVT_BUTTON, self.onOpenFile)
        # Create ListBox for HEAD numbers
        self.listBox = wx.ListBox(parent = leftPanel, choices = [], style = wx.LB_SINGLE | wx.LB_ALWAYS_SB)
        self.listBox.Bind(wx.EVT_LISTBOX, self.onSelectHEAD)
         # Add panels to Left Window BoxSizer
        leftBox.Add(openFileDlgBtn, proportion = 0, flag = wx.ALIGN_CENTER | wx.TOP, border = 10)
        leftBox.Add(self.listBox, proportion = 1, flag = wx.EXPAND | wx.ALIGN_LEFT | wx.TOP, border = 10)
        leftPanel.SetSizer(leftBox)

        # Add graph to Middle Window
        figure = Figure()
        self.canvas = FigureCanvas(self.middlePanel, -1, figure)
        middleBox.Add(self.canvas, proportion = 7, flag = wx.EXPAND | wx. ALIGN_CENTRE)

        # Add graph info panel to Middle Window
        infoPanel = wx.Panel(parent = self.middlePanel)
        infoBox = wx.BoxSizer(wx.HORIZONTAL)
        # Add text portion of graph info panel
        self.graphInfo = wx.TextCtrl(parent = infoPanel, value = "", style = wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_LEFT)
        infoBox.Add(self.graphInfo, proportion = 9, flag = wx.EXPAND | wx.ALIGN_LEFT | wx.RIGHT, border = 5)
        infoPanel.SetSizer(infoBox)
        # Add save picture buttons
        savePicturePanel = wx.Panel(parent = infoPanel)
        savePictureBox = wx.BoxSizer(wx.VERTICAL)
        # Create button for saving one picture
        savePictureBtn = wx.Button(parent = savePicturePanel, label = "Save picture of graph")
        savePictureBtn.Bind(wx.EVT_BUTTON, self.onSavePicture)
        savePictureBox.AddStretchSpacer(1);
        savePictureBox.Add(savePictureBtn, proportion = 2, flag = wx.EXPAND | wx.ALIGN_CENTRE)
        savePictureBox.AddStretchSpacer(1);
        # Create button for saving all pictures
        saveAllPicturesBtn = wx.Button(parent = savePicturePanel, label = "Save all pictures")
        saveAllPicturesBtn.Bind(wx.EVT_BUTTON, self.onSaveAllPictures)
        savePictureBox.Add(saveAllPicturesBtn, proportion = 2, flag = wx.EXPAND | wx.ALIGN_CENTRE)
        savePictureBox.AddStretchSpacer(10);
        # Add save picture panel to info panel
        savePicturePanel.SetSizer(savePictureBox)
        infoBox.Add(savePicturePanel, proportion = 2, flag = wx.EXPAND)
        # Add infoPanel to middleBox
        middleBox.Add(infoPanel, proportion = 2, flag = wx.EXPAND | wx.TOP | wx.BOTTOM | wx.LEFT | wx.RIGHT, border = 5)
        self.middlePanel.SetSizer(middleBox)

        # Add limit settings to right graph
        rightBox = wx.BoxSizer(wx.VERTICAL)
        # Add DEV limits
        panelDEV = wx.Panel(parent = self.rightPanel)
        sizerDEV = wx.BoxSizer(wx.HORIZONTAL)
        textDEV = wx.StaticText(parent = panelDEV, label = "Input limit for DEV value: ")
        self.textEntryDEV = wx.TextCtrl(parent = panelDEV)
        sizerDEV.Add(textDEV, proportion = 2)
        sizerDEV.Add(self.textEntryDEV, proportion = 4)
        panelDEV.SetSizer(sizerDEV)
        # Add RMS limits
        panelRMS = wx.Panel(parent = self.rightPanel)
        sizerRMS = wx.BoxSizer(wx.HORIZONTAL)
        textRMS = wx.StaticText(parent = panelRMS, label = "Input limit for RMS value: ")
        self.textEntryRMS = wx.TextCtrl(parent = panelRMS)
        sizerRMS.Add(textRMS, proportion = 2)
        sizerRMS.Add(self.textEntryRMS, proportion = 4)
        panelRMS.SetSizer(sizerRMS)
        # Add button for generating graphs based on limits
        generateLimitGraphsBtn = wx.Button(parent = self.rightPanel, label = "Generate graphs for selected limits")
        generateLimitGraphsBtn.Bind(wx.EVT_BUTTON, self.onGenerateLimitGraphs)
        # Add panels to rightBox
        rightBox.AddStretchSpacer(1)
        rightBox.Add(panelDEV, proportion = 3, flag = wx.EXPAND)
        rightBox.AddStretchSpacer(1)
        rightBox.Add(panelRMS, proportion = 3, flag = wx.EXPAND)
        rightBox.AddStretchSpacer(1)
        rightBox.Add(generateLimitGraphsBtn, proportion = 2, flag = wx.ALIGN_RIGHT)
        rightBox.AddStretchSpacer(1)
        # Add individual summary graphs
        self.summaryPanel = wx.Panel(parent = self.rightPanel)
        summaryBox = wx.BoxSizer(wx.HORIZONTAL)
        self.summaryCanvas = FigureCanvas(self.summaryPanel, 1, Figure())
        summaryBox.Add(self.summaryCanvas, proportion = 1, flag = wx.EXPAND | wx. ALIGN_CENTRE | wx.ALL)
        self.summaryPanel.SetSizer(summaryBox)
        rightBox.Add(self.summaryPanel, proportion = 90, flag = wx.EXPAND | wx. ALIGN_CENTRE | wx.ALL)
        # Add spacing at end
        rightBox.AddStretchSpacer(1)
        self.rightPanel.SetSizer(rightBox)

    # Event handler for FileDialog button
    def onOpenFile(self, event):
        # Creates file dialog window
        dlg = wx.FileDialog(
            self, message = "Choose a file",
            defaultDir = os.getcwd(),
            defaultFile = "",
            wildcard = "CSV files (*.csv)|*.csv",
            style = wx.FD_OPEN | wx.FD_CHANGE_DIR
            )
        # Show the selected files
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            print "You chose the following file(s):"
            for path in paths:
                print path
            self.ReadInData(filePath = dlg.GetPath())
        dlg.Destroy()

    # Event handler for when HEAD is selected from ListBox
    def onSelectHEAD(self, event):
        index = self.listBox.GetString(self.listBox.GetSelection()).split(":")[0]
        self.currentID = int(index)
        if(self.currentID is not None):
            self.master[self.currentID].DeleteData()
        self.ReadInHEAD(self.currentID)
        self.PlotGraph()
        self.UpdateGraphInfo()

    # Event handler for when save picture button is selected
    def onSavePicture(self, event):
        if self.currentFilePath is None:
            return
        if self.currentID is None:
            return
        path = os.getcwd() + "/head_images"
        if not os.path.exists(path):
            os.makedirs(path)
        imgPath = path + "/" + str(self.master[self.currentID].id) + "_" + self.master[self.currentID].serial_num
        if os.path.exists(imgPath):
            os.remove(imgPath)
        graph = self.master[self.currentID].PlotGraph()
        graph.set_canvas(self.canvas)
        graph.savefig(imgPath)
        print "Saved " + str(self.master[self.currentID].id) + ": " + self.master[self.currentID].serial_num + " as PNG image"

    # Event handler for when save all pictures button is selected
    def onSaveAllPictures(self, event):
        if self.currentFilePath is None:
            return
        path = os.getcwd() + "/head_images"
        if os.path.exists(path):
            shutil.rmtree(path)
        path = os.getcwd() + "/head_images_all/"
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)
        for index in self.master:
            HEAD = self.master[index]
            imgPath = path + "/" + str(HEAD.id) + "_" + HEAD.serial_num
            self.ReadInHEAD(HEAD.id)
            graph = HEAD.PlotGraph()
            graph.set_canvas(self.canvas)
            graph.savefig(imgPath)
            HEAD.DeleteData()
        print "Saved images of all HEADs"

    # Event handler for when generate limit graphs button is selected
    def onGenerateLimitGraphs(self, event):
        if self.currentFilePath is None:
            return
        try:
            dev_limit = float(self.textEntryDEV.GetLineText(0))
            rms_limit = float(self.textEntryRMS.GetLineText(0))
        except ValueError:
            #TODO create ALERT
            return
        results = ReadCSVWithLimit(self.currentFilePath, dev_limit, rms_limit)
        self.summary = Summary(numHEADs = len(self.master), dev = results[0], rms = results[1])
        self.summaryCanvas = FigureCanvas(self.summaryPanel, 1, self.summary.PlotSummaryGraphs())

    # Checks if file is valid and calls necessary read function
    def ReadInData(self, filePath):
        if(filePath[-4:] == ".csv"):
            self.master = ReadInitialCSVFile(filePath)
            self.currentFilePath = filePath
            keys = self.master.keys()
            keys.sort()
            items = map(str,keys)
            items = [key + ": " + self.master[int(key)].serial_num for key in items]
            self.listBox.InsertItems(items,0)
        else:
            raise ValueError("wrong file type selected")

    # Reads in HEAD data based on selection by user
    def ReadInHEAD(self, id):
        lineNum = self.master[id].line_num
        headings = self.master[id].data_headings
        self.master[id].data = ReadInHEADData(self.currentFilePath, headings, lineNum)

    # Plots graph based on selected id
    def PlotGraph(self):
        self.canvas = FigureCanvas(self.middlePanel, 1, self.master[self.currentID].PlotGraph())

    # Updates the information below the display of the graph
    def UpdateGraphInfo(self):
        description = self.master[self.currentID].description
        headings = self.master[self.currentID].description_headings
        info = ""
        num = 0
        while num < len(description):
            info = info + headings[num] + ": " + description[num] + "\n"
            num = num + 1
        self.graphInfo.SetValue(info)

# Initialize main
if __name__ == '__main__':
    app = wx.App()
    MainWindow(parent = None,
            style = wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER |
                    wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX,
            title = 'Western Digital HEAD Data Processing')
    app.MainLoop()
