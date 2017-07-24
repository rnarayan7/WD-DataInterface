import pandas as pd
import matplotlib as plt
import wx
import os
from reader import readInitialCSVFile
from reader import readInHEAD

# Main window class
class MainWindow(wx.Frame):
    def __init__(self,parent,style,title):
        super(MainWindow, self).__init__(parent, title = title,
            style = style, size = wx.Size(1200,800))
        self.InitUI()
        self.Centre()
        self.Show()
        self.master = {}
        #self.currentID
        #self.currentFilePath
        #self.listBox

    # Initialize the UI
    def InitUI(self):
        panel = wx.Panel(self)
        mainBox = wx.BoxSizer(wx.HORIZONTAL)
        leftBox = wx.BoxSizer(wx.VERTICAL)
        # Initialize panels
        bottomPanel = wx.Panel(parent = panel, style = wx.DOUBLE_BORDER)
        rightPanel = wx.Panel(parent = panel, style = wx.DOUBLE_BORDER)
        leftPanel = wx.Panel(parent = panel, style = wx.DOUBLE_BORDER)
        # Add components to Main Window BoxSizer
        mainBox.Add(leftPanel, proportion = 1, flag = wx.EXPAND | wx.ALIGN_CENTER | wx.LEFT, border = 20)
        mainBox.Add(bottomPanel, proportion = 1, flag = wx.EXPAND | wx.ALIGN_CENTER | wx.BOTTOM, border = 20)
        mainBox.Add(rightPanel, proportion = 1, flag = wx.EXPAND | wx.ALIGN_CENTER | wx.RIGHT, border = 20)
        panel.SetSizer(mainBox)
        # Create FileDialog button
        openFileDlgBtn = wx.Button(parent = leftPanel, label = "Select a data file")
        openFileDlgBtn.Bind(wx.EVT_BUTTON, self.onOpenFile)
        # Create ListBox for HEAD numbers
        self.listBox = wx.ListBox(parent = leftPanel, choices = [], style = wx.LB_SINGLE | wx.LB_ALWAYS_SB)
         # Add panels to Left Window BoxSizerBHORA
        leftBox.Add(openFileDlgBtn, proportion = 0, flag = wx.ALIGN_CENTER | wx.TOP, border = 10)
        leftBox.Add(self.listBox, proportion = 1, flag = wx.EXPAND | wx.ALIGN_LEFT | wx.TOP, border = 10)
        leftPanel.SetSizer(leftBox)

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
            self.readInData(filePath = dlg.GetPath())
        dlg.Destroy()

    # Checks if file is valid and calls necessary read function
    def readInData(self, filePath):
        if(filePath[-4:] == ".csv"):
            self.master = readInitialCSVFile(filePath)
            self.currentFilePath = filePath
            keys = self.master.keys()
            keys.sort()
            self.listBox.InsertItems(map(str, keys),0)
        else:
            raise ValueError("wrong file type selected")
    
    # Reads in HEAD data based on selection by user
    def readInHEAD(self, id):
        self.currentID = id
        lineNum = self.master[self.currentID].line_num
        headings = self.master[self.currentID].headings
        self.master[self.currentID].data = readInHEAD(self.currentFilePath, headings, lineNum)

# Initialize main
if __name__ == '__main__':
    app = wx.App()
    MainWindow(parent = None,
            style = wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER |
                    wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX,
            title = 'Western Digital HEAD Data Processing')
    app.MainLoop()
