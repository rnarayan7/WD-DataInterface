import wx
import os

from reader import ReadInitialCSVFile
from reader import ReadInHEADData

import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

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
        #self.plt
        #self.figure

    # Initialize the UI
    def InitUI(self):
        panel = wx.Panel(self)
        mainBox = wx.BoxSizer(wx.HORIZONTAL)
        leftBox = wx.BoxSizer(wx.VERTICAL)
        middleBox = wx.BoxSizer(wx.VERTICAL)
        # Initialize panels
        self.middlePanel = wx.Panel(parent = panel, style = wx.DOUBLE_BORDER)
        rightPanel = wx.Panel(parent = panel, style = wx.DOUBLE_BORDER)
        leftPanel = wx.Panel(parent = panel, style = wx.DOUBLE_BORDER)
        # Add components to Main Window BoxSizer
        mainBox.Add(leftPanel, proportion = 1, flag = wx.EXPAND | wx.ALIGN_CENTER | wx.LEFT, border = 10)
        mainBox.Add(self.middlePanel, proportion = 3, flag = wx.EXPAND | wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, border = 5)
        mainBox.Add(rightPanel, proportion = 1, flag = wx.EXPAND | wx.ALIGN_CENTER | wx.RIGHT, border = 10)
        panel.SetSizer(mainBox)
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
        # Add panels to Middle Window
        figure = Figure()
        self.canvas = FigureCanvas(self.middlePanel, -1, figure)
        middleBox.Add(self.canvas, proportion = 1, flag = wx.EXPAND)
        self.middlePanel.SetSizer(middleBox)
    
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
        self.ReadInHEAD(int(index))
        self.PlotGraph()

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
        if(self.currentID is not None):
            self.master[self.currentID].DeleteData()
        self.currentID = id
        lineNum = self.master[self.currentID].line_num
        headings = self.master[self.currentID].data_headings
        self.master[self.currentID].data = ReadInHEADData(self.currentFilePath, headings, lineNum)
    
    # Plots graph based on selected id
    def PlotGraph(self):
        currentData = self.master[self.currentID].data
        if(currentData is None):
            raise ValueError("data frame empty")
            return
        figure = Figure(figsize = (8.5,7))
        plt = figure.add_axes([0.1,0.1,0.8,0.8])
        plt.plot(currentData["TS_TFCSetup_AE_Sensor_DEV"],'b')
        plt.plot(currentData["TS_TFCSetup_AE_Sensor_NMC"],'r')
        plt.plot(currentData["TS_TFCSetup_AE_Sensor_RMS"],'k')
        plt.legend()
        plt.set_xlabel("TFC Power (mW)")
        plt.set_title(self.master[self.currentID].serial_num)
        self.canvas = FigureCanvas(self.middlePanel, -1, figure)

# Initialize main
if __name__ == '__main__':
    app = wx.App()
    MainWindow(parent = None,
            style = wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER |
                    wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX,
            title = 'Western Digital HEAD Data Processing')
    app.MainLoop()
