import tkinter
from tkinter.constants import CENTER
from tkinter.ttk import *
import Test
import mdfParser
import models
import os
import numpy as np

poly = None
effModel = None
powModel = None

def runSimulation():
    fileName = fileEntry.get()
    fileCreatedLabel.place(relx = .5, rely = .23, anchor = CENTER)
    if not len(fileName):
        fileCreatedLabel.config(text = "Must have a File Name")
        return

    Test.makeMDF(fileName)
    fileCreatedLabel.config(text = "File Created")

    powModel, effModel, poly = models.makeModel(fileName + "//" + fileName)
    
def predictMax():
    bestEff, bestEffPoint = models.getMax((effModel, poly))
    bestPow, bestPowPoint = models.getMax((powModel, poly))
    
    #print

def predictPoint():
    predictErrorLabel.place_forget()
    x = predictx.get()
    y = predicty.get()
    try: 
        float(x)
        float(y)
    except:
        predictErrorLabel.place(relx = .5, rely = .94, anchor = CENTER)
        return
    if float(x) < -.8 or float(x) > .8 or float(y) < -.8 or float(y) > .8:
        predictErrorLabel.place(relx = .5, rely = .94, anchor = CENTER)
        return
    X_transform = poly.fit_transform(np.array([[x, y]]))
    predictEff = effModel.predict(X_transform)
    predictPow = powModel.predict(X_transform)
    #print
    
def printEffGraph():
    models.printGraph(effModel)

def printPowGraph():
    models.printGraph(powModel)

GUI = tkinter.Tk()
GUI.title("Machine Learning for Load Pull Simulations")
GUI.geometry("300x400")
GUI.resizable(False, False)

fileEntry = Entry(GUI, width = 20)
fileEntry.place(relx = .5, rely = .05, anchor = CENTER)

entryButton = tkinter.ttk.Button(GUI, text = "Submit File Name", width = 20, command = runSimulation)
entryButton.place(relx = .5, rely = .15, anchor = CENTER)

fileCreatedLabel = tkinter.Label(GUI)

showEffGraphButton = tkinter.ttk.Button(GUI, text = "Show Efficiency Graph", command = printEffGraph, width = 20)
showEffGraphButton.place(relx = .25, rely = .3, anchor = CENTER)

showPowGraphButton = tkinter.ttk.Button(GUI, text = "Show Power Graph", command = printPowGraph, width = 20)
showPowGraphButton.place(relx = .75, rely = .3, anchor = CENTER)

button = tkinter.ttk.Button(GUI, text = "Get Max Power and Efficiency Points", width = 40, command = predictMax)
button.place(relx = .5, rely = .45, anchor = CENTER)

predictButton = tkinter.ttk.Button(GUI, text = "Predict Power and Efficiency at Point", width = 40, command = predictPoint)
predictButton.place(relx = .5, rely = .7, anchor = CENTER)

xlabel = tkinter.Label(GUI, text = "x")
xlabel.place(relx = .3, rely = .77, anchor = CENTER)

ylabel = tkinter.Label(GUI, text = "y")
ylabel.place(relx = .7, rely = .77, anchor = CENTER)

predictx = Entry(GUI, width = 10)
predictx.place(relx = .3, rely = .84, anchor = CENTER)

predicty = Entry(GUI, width = 10)
predicty.place(relx = .7, rely = .84, anchor = CENTER)

predictErrorLabel = tkinter.Label(GUI, text = "Invalid inputs (x and y must be -0.8 to 0.8)")

predictXLabel = tkinter.Label(GUI)
predictXLabel.place(anchor = CENTER, relx = .25, rely = .93)

predictYLabel = tkinter.Label(GUI)
predictYLabel.place(anchor = CENTER, relx = .75, rely = .93)

GUI.mainloop()