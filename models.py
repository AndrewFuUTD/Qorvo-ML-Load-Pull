import numpy as np
from numpy.core.arrayprint import str_format 
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def convert(ar):
    for x in range(len(ar)):
        ar[x] = ar[x][0]
    return ar

def makeModel(file):
    df = pd.read_csv(file, usecols = ['gammaTuple','power','harmonic', 'a1','b1','a2','b2',
    'V1','I1','V2','I2','Pin','Pout','Gain','Pdc1', 'Pdc2', 'PAE', 'Load Gamma', 'r', 'x']) 
    #df = df.sample(frac=1,replace = Fals)
    X = df[df['harmonic'] == 1]
    X = X[X['power'] == 7]
    pointsR = X[[ 'r']].values.tolist()
    pointsZ = X[['x']].values.tolist()
    pointsX = X[[ 'r', 'x']].values.tolist()
    powerPointsY = X[[ 'Pout']].values.tolist()
    efficiencyPointsY = X[['PAE']].values.tolist()

    powerPoints = convert(powerPointsY)
    efficiencyPoints = convert(efficiencyPointsY)
    pointsR = convert(pointsR)
    pointsZ = convert(pointsZ)

    linregPower = LinearRegression()
    linregEfficiency = LinearRegression()
    poly = PolynomialFeatures(5)
    X_transform = poly.fit_transform(pointsX)
    linregPower.fit(X_transform,powerPoints)
    linregEfficiency.fit(X_transform,efficiencyPoints)

    return linregPower, linregEfficiency, poly

def printGraph(model):
    linreg = model[0]
    poly = model[1]

    space = np.linspace(-.8, .8, 100)
    gridX,gridR = np.meshgrid(space,space)

    predictions = []

    for x in gridX[0]:
        temp = []
        for r in gridR:
            point = np.array([[x,r[0]]])
            X_test_transform = poly.fit_transform(point)
            y_preds = linreg.predict(X_test_transform)[0]
            temp.append(y_preds)
        predictions.append(temp)

    ANGLE = 90
    ROTATION = 30
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    surf1 = ax.plot_surface(gridX,gridR,np.array(predictions), rstride=1, cstride=1,cmap='viridis', edgecolor='none')
    ax.set_xlabel('X')
    ax.set_ylabel('R')
    ax.set_zlabel('Efficiency')
    plt.title("Polynomial Regression")
    ax.view_init(ANGLE,ROTATION)
    plt.colorbar(surf1)
    plt.show()

def getMax(model):

    space = np.linspace(-.8, .8, 100)     
    gridX, gridR = np.meshgrid(space,space)

    linreg = model[0]
    poly = model[1]

    predictions = []
    bestPrediction = 0
    bestPoint = None 

    for x in gridX[0]:
        temp = []
        for r in gridR:
            point = np.array([[x,r[0]]])
            X_test_transform = poly.fit_transform(point)
            y_preds = linreg.predict(X_test_transform)[0]
            temp.append(y_preds)
            if y_preds > bestPrediction:
                bestPrediction = y_preds
                bestP = point
        predictions.append(temp)

    return bestPrediction, bestPoint


