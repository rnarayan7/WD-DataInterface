import wx
import os
import shutil

from reader import ReadInitialCSVFile
from reader import ReadInHEADData

import matplotlib
import matplotlib.pyplot
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
        #figure
        #self.middlePanel
        #self.graphInfo
        #self.rightPanel
        #self.textEntryDEV
        #self.textEntryRMS

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
        warningInfo = wx.StaticText(parent = self.rightPanel, label = "Note: this is a time-intensive operation, so use only when necessary")
        font = wx.Font(12, family = wx.DECORATIVE, style = wx.ITALIC, weight = wx.NORMAL)
        warningInfo.SetFont(font)
        # Add panels to rightBox 
        rightBox.AddStretchSpacer(1) #TEMPORARY
        rightBox.Add(panelDEV, proportion = 3, flag = wx.EXPAND)
        rightBox.AddStretchSpacer(1) #TEMPORARY
        rightBox.Add(panelRMS, proportion = 3, flag = wx.EXPAND)
        rightBox.AddStretchSpacer(1) #TEMPORARY
        rightBox.Add(generateLimitGraphsBtn, proportion = 2, flag = wx.ALIGN_RIGHT)
        rightBox.AddStretchSpacer(1) #TEMPORARY
        rightBox.Add(warningInfo, proportion = 2, flag = wx.ALIGN_RIGHT)
        rightBox.AddStretchSpacer(90) #TEMPORARY
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
        print "Do nothing so far"
    
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
        self.canvas = FigureCanvas(self.middlePanel, -1, self.master[self.currentID].PlotGraph())
    
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
