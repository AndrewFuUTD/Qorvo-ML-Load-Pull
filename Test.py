import win32com.client
import os
import mdfParser

def makeMDF(fileName):

    
    awrde = win32com.client.Dispatch('MWOApp.MWOffice')
    g = awrde.Project.Schematics(1)
    g = awrde.Project.DataFiles(1)

    newDirectory = os.getcwd()
    newFilePath = os.path.join(newDirectory, fileName)
    os.mkdir(newFilePath)

    fp = os.getcwd() + "\\" + fileName + "\\" + fileName + ".mdf"
    g.Export(fp)
    mdfParser.readMDF(fileName)
    g = awrde.Project.Graphs("PAE and Output Power Contours at X dB Compression")