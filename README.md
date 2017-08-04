# WD-DataInterface
Data visualization software for Western Digital data from HEADs

Features:
  - reads CSV files containing information about Western Digital disk HEADs
  - allows user to select individual HEADs and displays graphs of DEV, NMC, and RMS sensor readings with respect to power applied
  - allows user to save PNG pictures of graphs created in directory of program
  - provides histogram of the power supplied to the HEADs before sensors cross a certain limit/threshold

Design:
  - GUI built using WXPython package
  - Uses Matplotlib for creation of graphs
  - Uses CSV parser and reader for accessing data
