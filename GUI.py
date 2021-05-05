import tkinter
from tkinter.constants import CENTER
from tkinter.ttk import *
import Test
import mdfParser
#import models
import os

GUI = tkinter.Tk()
GUI.title("Machine Learning for Load Pull Simulations")
GUI.geometry("300x350")
GUI.resizable(False, False)

button = tkinter.Button(GUI, text = "Get Max Power", width = 15, height = 5, bg = "blue", fg = "white")
button.place(relx = .1, rely = .5)

button1 = tkinter.Button(GUI, text = "Get Max Efficiency", width = 15, height = 5, bg = "black", fg = "yellow")
button1.place(relx = .5, rely = .5)

w = Entry(GUI, width = 20)
w.place(relx = .5, rely = .1, anchor = CENTER)

errorLabel = tkinter.Label(GUI, text = "Must have a file name")
fileCreatedLabel = tkinter.Label(GUI, text = "Files created")

def runSimulation():
    errorLabel.place_forget()
    fileCreatedLabel.place_forget()
    fileName = w.get()
    if not len(fileName):
        errorLabel.place(relx = .5, rely = .4, anchor = CENTER)
        return
    fileCreatedLabel.place(relx = .5, rely = .4, anchor = CENTER)

    Test.makeMDF(fileName)
    models.makeModel

    


entryButton = tkinter.Button(GUI, text = "Submit File Name", width = 15, height = 3, bg = "red", fg = "black", command = runSimulation)
entryButton.place(relx = .5, rely = .25, anchor = CENTER)


GUI.mainloop()