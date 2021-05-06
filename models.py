import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


def convert(ar):
    for x in range(len(ar)):
        ar[x] = ar[x][0]
    return ar

def printML(mod, gridR,gridX,name):
    predictions = []
    bestPoint = None
    bestPrediction = 0
    for x in gridX[0]:
        temp = []
        for r in gridR:
            p = r[0]
            point = np.array([[x,p]])
            pred = mod.predict(point)
            if pred > bestPrediction:
                bestPrediction = pred
                bestPoint = point
            temp.append(pred[0])
        predictions.append(temp)
    print(name, bestPoint,bestPrediction)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    surf1 = ax.plot_surface(gridX,gridR,np.array(predictions), rstride=1, cstride=1,
                cmap='viridis', edgecolor='none')
    ax.set_xlabel('X')
    ax.set_ylabel('R')
    ax.set_zlabel('Efficiency')
    plt.title(name)
    ax.view_init(90,30)
    plt.colorbar(surf1)
    plt.show()

def makeModel():
    df = pd.read_csv('2\\2.csv', usecols = ['gammaTuple','power','harmonic', 'a1','b1','a2','b2',
    'V1','I1','V2','I2','Pin','Pout','Gain','Pdc1', 'Pdc2', 'PAE', 'Load Gamma', 'r', 'x']) 
    #df = df.sample(frac=1,replace = Fals)

    X = df[df['harmonic'] == 1]
    X = X[X['power'] == 7]

    pointsR = X[[ 'r']].values.tolist()
    pointsZ = X[['x']].values.tolist()
    pointsX = X[[ 'r', 'x']].values.tolist()
    powerPointsY = X[[ 'Pout']].values.tolist()
    efficiencyPointsY = X[['PAE']].values.tolist()
    bestPoint = np.array([[0.08713,0.07129]])
    powerPointsY = convert(powerPointsY)
    efficiencyPointsY = convert(efficiencyPointsY)
    pointsR = convert(pointsR)
    pointsZ = convert(pointsZ)
    smallestR = np.amin(np.array(pointsR))
    smallestZ = np.amin(np.array(pointsZ))
    largestR = np.amax(np.array(pointsR))
    largestZ = np.amax(np.array(pointsZ))
    gridX = np.linspace(smallestR, largestR, 100)
    gridR = np.linspace(smallestZ, largestZ, 100)
    gridX,gridR = np.meshgrid(gridX,gridR)
    reg = LinearRegression()
    reg.fit(pointsX,efficiencyPointsY)
    printML(reg, gridR,gridX,'Linear Regression')

    linreg = LinearRegression()
    poly = PolynomialFeatures(50)
    X_transform = poly.fit_transform(pointsX)
    p = linreg.fit(X_transform,efficiencyPointsY)
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
                bestPoint = point
        predictions.append(temp)

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    surf1 = ax.plot_surface(gridX,gridR,np.array(predictions), rstride=1, cstride=1,cmap='viridis', edgecolor='none')
    ax.set_xlabel('X')
    ax.set_ylabel('R')
    ax.set_zlabel('Efficiency')
    plt.title('Polynomial Regression')
    ax.view_init(90,30)
    plt.colorbar(surf1)
    plt.show()

    return bestPrediction





