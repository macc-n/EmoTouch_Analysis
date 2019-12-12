# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 12:22:11 2019

@author: robby
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import math
import numpy.linalg as la
from sklearn import preprocessing
import BaseFunctions as bf


#metodo per trovare il value più vicino in un array di values

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

#metodo che legge i punti di cambio di direzione.
"""
input: actionsInfo = dataframe con tutti i tocchi
output: datafrane con le coordinate dei punti, delta time e l'index originario del dataframe iniziale
"""
def getDirectionChangingPoints(actionsInfo):
    actionsInfo = bf.aggiungiDeltaTimeTraPunti(actionsInfo)
    
    #calcolo i tetha tra tutti i punti del pattern -filter non specificato imp. 360°- per poi filtrare i picchi
    deltaDataFrame = pd.DataFrame(columns=['tetha','Time'])
    acInfo = actionsInfo[[2,3,'Time','oldIndex']]
    acInfo = acInfo.rename(columns = {2: 'X', 3: 'Y'})
    print(acInfo)
    deltaDataFrame = bf.anglesBetweenThreePoints(acInfo)
    
    #normalizzo i valori tetha
    min_max_scaler = preprocessing.MinMaxScaler()
    deltaDataFrame[['tetha']] = min_max_scaler.fit_transform(deltaDataFrame[['tetha']].values)
        
    #aggiungo tetha al primo e ultimo punto in modo tale da avee un picco per leggere anche il primo angolo utile
    deltaDataFrame = bf.addFirstLastPoints(actionsInfo, deltaDataFrame, add='values')

    picchiMinimi = argrelextrema(deltaDataFrame.iloc[:,0].values, np.less) #massimi con np.greater
    picchiMassimi = argrelextrema(deltaDataFrame.iloc[:,0].values, np.greater)

    picchiDataFrame = pd.DataFrame(columns = ['X','Y','Time','oldIndex'])
    if(picchiMinimi[0].size != 0 and picchiMassimi[0].size != 0):
        for n in picchiMinimi[0]:
            val = actionsInfo.loc[actionsInfo.index[actionsInfo['Time'] == deltaDataFrame.iloc[n][1]]]
            temp = pd.DataFrame([[val[2].values[0], val[3].values[0], val['Time'].values[0], val['oldIndex'].values[0]]], columns = ['X','Y','Time','oldIndex'])
            picchiDataFrame = picchiDataFrame.append(temp, ignore_index=True)
        
        for n in picchiMassimi[0]:            
            val = actionsInfo.loc[actionsInfo.index[actionsInfo['Time'] == deltaDataFrame.iloc[n][1]]]
            temp = pd.DataFrame([[val[2].values[0], val[3].values[0], val['Time'].values[0], val['oldIndex'].values[0]]], columns = ['X','Y','Time','oldIndex'])
            picchiDataFrame = picchiDataFrame.append(temp, ignore_index=True)
    else:
        for n in range(0,len(deltaDataFrame.index)):
            val = actionsInfo.loc[actionsInfo.index[actionsInfo['Time'] == deltaDataFrame.iloc[n][1]]]
            temp = pd.DataFrame([[val[2].values[0], val[3].values[0], val['Time'].values[0], val['oldIndex'].values[0]]], columns = ['X','Y','Time','oldIndex'])
            picchiDataFrame = picchiDataFrame.append(temp, ignore_index=True)
    
    picchiDataFrame = bf.addFirstLastPoints(actionsInfo, picchiDataFrame, add='coords')

    picchiDataFrame = picchiDataFrame.drop_duplicates(subset=['Time'], keep='first')

    anglePoints = bf.anglesBetweenThreePoints(picchiDataFrame, filter=135)
    anglePoints = bf.addFirstLastPoints(actionsInfo, anglePoints, add='coords')
    
    #print("AnglePoints")
    #print(anglePoints)
    
    return anglePoints
#metodo per disegnare il pattern con i punti di cambio di direzione 
"""
input: tocchi del pattern, punti di cambio, path per il nome del grafico, inverti si/no indica se proiettare il pattern
con l'origine in basso a sinistra o in alto (gli smartphone hanno l'origine in alto a sinistra)
"""
def drawPoints(actionsInfo, anglePoints, path, inverti='si'):

    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 9
    fig_size[1] = 6
    plt.rcParams["figure.figsize"] = fig_size
    
    fig = plt.figure()
    #fig.suptitle("Valori normalizzati") angolo teta
    fig, ax_lst = plt.subplots(1, 1)
    if inverti == 'si':
        #inverte asse y
        plt.gca().invert_yaxis()
        #sposta asse x sopra (per comodità di lettura)
        ax_lst.xaxis.tick_top()
        #ax_lst.xaxis.set_ticks([1.,2.,3.,10.])
    ax_lst.grid(True)
    #plt.scatter(deltaDataFrame.iloc[:,1], deltaDataFrame.iloc[:,0],  label="Speed")
    plt.title(path)
    plt.plot(actionsInfo.iloc[:,2], actionsInfo.iloc[:,3],  color='black', label="Angles")
    plt.scatter(actionsInfo.iloc[:,2], actionsInfo.iloc[:,3],  color='black',  label="Angles")
    #plt.plot(anglePoints.iloc[[6,7],[0]], anglePoints.iloc[[6,7],[1]],  color='red', label="Angles")
    #plt.scatter(anglePoints.iloc[[6,7],[0]], anglePoints.iloc[[6,7],[1]],  color='red',  label="Angles")
    plt.plot(anglePoints.iloc[:,0], anglePoints.iloc[:,1],  color='red',  label="Angles")
    plt.scatter(anglePoints.iloc[:,0], anglePoints.iloc[:,1],  color='red',  label="Angles")
    #plt.title("Pattern difficile 2, matricola 656883")
    #plt.legend()   
    plt.show()

    return fig
