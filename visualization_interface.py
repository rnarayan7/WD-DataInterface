import pandas as pd
import matplotlib as plt
import wx
import os
import csv

# Main window class
class MainWindow(wx.Frame):
    def __init__(self,parent,style,title):
        super(MainWindow, self).__init__(parent, title = title,
            style = style, size = wx.Size(1200,800))
        self.InitUI()
        self.Centre()
        self.Show()

    # Initialize the UI
    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.HORIZONTAL)
        # Initialize panels
        bottomPanel = wx.Panel(parent = panel, style = wx.DOUBLE_BORDER)
        rightPanel = wx.Panel(parent = panel, style = wx.DOUBLE_BORDER)
        leftPanel = wx.Panel(parent = panel, style = wx.DOUBLE_BORDER)
        # Add panels to BoxSizer
        vbox.Add(rightPanel, proportion = 1, flag = wx.EXPAND | wx.RIGHT | wx.ALIGN_CENTER, border = 20)
        vbox.Add(bottomPanel, proportion = 1, flag = wx.EXPAND | wx.BOTTOM | wx.ALIGN_CENTER, border = 20)
        vbox.Add(leftPanel, proportion = 1, flag = wx.EXPAND | wx.LEFT | wx.ALIGN_CENTER, border = 20)
        panel.SetSizer(vbox)
        # Add FileDialog button
        openFileDlgBtn = wx.Button(panel, label = "Select a data file")
        openFileDlgBtn.Bind(wx.EVT_BUTTON, self.onOpenFile)
        # Add HEAD numbers in left panel

    # Event handler for FileDialog button
    def onOpenFile(self, event):
        # Creates file dialog window
        dlg = wx.FileDialog(
            self, message = "Choose a file",
            defaultDir = os.getcwd(),
            defaultFile = "",
            wildcard = "CSV files (*.csv)|*.csv|Excel files (*.xlsx)|*.xlsx",
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

    def readInData(self, filePath):
        print "reached" #DELETE
        if(filePath[:-5] == ".xlsx"):
            data = pd.read_excel(filePath)
        elif(filePath[:-4] == ".csv"):
            data = pd.read_csv(filePath)

# Initialize main
if __name__ == '__main__':
    app = wx.App()
    MainWindow(parent = None,
            style = wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER |
                    wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX,
            title = 'Western Digital HEAD Data Processing')
    app.MainLoop()
