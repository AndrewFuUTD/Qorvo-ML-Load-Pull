import tkinter
from tkinter.constants import CENTER
from tkinter.ttk import *
import Test
import mdfParser
import models
import os

def runSimulation():
    errorLabel.place_forget()
    fileCreatedLabel.place_forget()
    fileName = fileEntry.get()
    if not len(fileName):
        errorLabel.place(relx = .5, rely = .35, anchor = CENTER)
        return
    fileCreatedLabel.place(relx = .5, rely = .35, anchor = CENTER)

    Test.makeMDF(fileName)
    models.makeModel()

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

GUI = tkinter.Tk()
GUI.title("Machine Learning for Load Pull Simulations")
GUI.geometry("300x370")
GUI.resizable(False, False)

fileEntry = Entry(GUI, width = 20)
fileEntry.place(relx = .5, rely = .1, anchor = CENTER)

entryButton = tkinter.ttk.Button(GUI, text = "Submit File Name", width = 20, command = runSimulation)
entryButton.place(relx = .5, rely = .25, anchor = CENTER)

errorLabel = tkinter.Label(GUI, text = "Must have a file name")
fileCreatedLabel = tkinter.Label(GUI, text = "Files created")

button = tkinter.ttk.Button(GUI, text = "Get Max Power and Efficiency Points", width = 40)
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



GUI.mainloop()