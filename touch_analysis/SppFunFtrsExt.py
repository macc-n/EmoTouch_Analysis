# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 09:28:15 2019

@author: robby
"""
import numpy as np
import pandas as pd
import time
import math
import BaseFunctions as bf
import AnglePointsExtractor as ape

#calcola le features
"""
input: dataframe tocchi e dataframe punti di cambio direzione
output: intero dataframe con le features su tutti gli swipe di un pattern
"""


def calculateTouchFeatures(actionsInfo, anglePoints):
    #print("actionsInfo")
    #print(actionsInfo)
    #print(actionsInfo.iloc[:,4])
    pd.set_option('display.max_columns',100)#righe max_rows
    lineaNumero = 1
    #intervalli = bf.calcolaIntervalli(data, np.array([30,70,100]))
    firstX = anglePoints.iloc[0][0]
    firstY = anglePoints.iloc[0][1]
    firstT = anglePoints.iloc[0][2]
    firstIdx = anglePoints.iloc[0][3]
    #print("anglePoints")
    #print(anglePoints)
    finalDF = pd.DataFrame([])
    for crdX, crdY, t, oldIdx in zip(anglePoints.iloc[1:,0], anglePoints.iloc[1:,1], anglePoints.iloc[1:,2], anglePoints.iloc[1:,3]):
        linea = "Linea"+str(lineaNumero)+"_"
        generalFeatures = pd.DataFrame(columns = [linea+'Distanza',linea+'Speed',linea+'DevLinea',linea+'VarPressione',linea+'VarSize',linea+'DirLinea'])
        percTocchiPPDirDF = pd.DataFrame(columns = [linea+'PercTocchiPPDir1',linea+'PercTocchiPPDir2',linea+'PercTocchiPPDir3',linea+'PercTocchiPPDir4',
                                                    linea+'PercTocchiPPDir5',linea+'PercTocchiPPDir6',linea+'PercTocchiPPDir7',linea+'PercTocchiPPDir8'])
        percTocchiSPDirDF = pd.DataFrame(columns = [linea+'PercTocchiSPDir1',linea+'PercTocchiSPDir2',linea+'PercTocchiSPDir3',linea+'PercTocchiSPDir4',
                                                    linea+'PercTocchiSPDir5',linea+'PercTocchiSPDir6',linea+'PercTocchiSPDir7',linea+'PercTocchiSPDir8'])
        percTocchiEPDirDF = pd.DataFrame(columns = [linea+'PercTocchiEPDir1',linea+'PercTocchiEPDir2',linea+'PercTocchiEPDir3',linea+'PercTocchiEPDir4',
                                                    linea+'PercTocchiEPDir5',linea+'PercTocchiEPDir6',linea+'PercTocchiEPDir7',linea+'PercTocchiEPDir8'])
        varTethaPPDirDF = pd.DataFrame(columns = [linea+'VarTethaPPDir1',linea+'VarTethaPPDir2',linea+'VarTethaPPDir3',linea+'VarTethaPPDir4',
                                                linea+'VarTethaPPDir5',linea+'VarTethaPPDir6',linea+'VarTethaPPDir7',linea+'VarTethaPPDir8'])
        varTethaSPDirDF = pd.DataFrame(columns = [linea+'VarTethaSPDir1',linea+'VarTethaSPDir2',linea+'VarTethaSPDir3',linea+'VarTethaSPDir4',
                                                linea+'VarTethaSPDir5',linea+'VarTethaSPDir6',linea+'VarTethaSPDir7',linea+'VarTethaSPDir8'])
        varTethaEPDirDF = pd.DataFrame(columns = [linea+'VarTethaEPDir1',linea+'VarTethaEPDir2',linea+'VarTethaEPDir3',linea+'VarTethaEPDir4',
                                                linea+'VarTethaEPDir5',linea+'VarTethaEPDir6',linea+'VarTethaEPDir7',linea+'VarTethaEPDir8'])
        varTethaAssiDF = pd.DataFrame(columns = [linea+'VarTethaAsseX',linea+'VarTethaAsseY'])
        percTocchiPPDirS = pd.Series([])
        percTocchiSPDirS = pd.Series([])
        percTocchiEPDirS = pd.Series([])
        varTethaPPDirS = pd.Series([])
        varTethaSPDirS = pd.Series([])
        varTethaEPDirS = pd.Series([])
        
        """
        print("intervallo")
        print(str(firstIdx)+"-"+str(oldIdx))
        print("X: "+str(firstX)+", Y: "+str(firstY)+", Time: "+str(firstT)+", oldIdx: "+str(firstIdx))
        print("X: "+str(crdX)+", Y: "+str(crdY)+", Time: "+str(t)+", oldIdx: "+str(oldIdx))
        """
        subActionsInfo = bf.getSubActionsInfo(actionsInfo, firstIdx, oldIdx)
        distanza = bf.getDistance(np.array([crdX,firstX]), np.array([crdY,firstY]))
        speed = distanza/(t-firstT)
        #invertire qui
        devLinea = distanza/(bf.calcolaDisplacemente(subActionsInfo))
        varPressione = np.var(subActionsInfo.iloc[:,4])
        varSize = np.var(subActionsInfo.iloc[:,5])
        
        angolo = math.degrees(np.arctan((crdY-firstY)/(crdX-firstX)))        
        if crdX < firstX:
            angolo += 180
        if angolo < 0:
            angolo += 360
            
        dirLinea = bf.getDirection(angolo)
        
        tethaAsseX = bf.anglesBetweenThreePoints(subActionsInfo[[2,3,'Time','oldIndex']], asse='x')
        tethaAsseY = bf.anglesBetweenThreePoints(subActionsInfo[[2,3,'Time','oldIndex']], asse='y')
        varTethaAsseX = np.var(tethaAsseX.iloc[:,0])
        varTethaAsseY = np.var(tethaAsseY.iloc[:,0])
        ppDirections = bf.angleDirectionTwoPoints(subActionsInfo[[2,3,'Time','oldIndex']], mode='pp')
        spDirections = bf.angleDirectionTwoPoints(subActionsInfo[[2,3,'Time','oldIndex']], mode='sp')
        epDirections = bf.angleDirectionTwoPoints(subActionsInfo[[2,3,'Time','oldIndex']], mode='ep')
        """
        print("ppDirections")
        print(ppDirections)
        print("spDirections")
        print(spDirections)
        print("epDirections")
        print(epDirections)
        """
        for x in range (1, 9):
            varTethaPPDir = np.var(ppDirections.iloc[:,0].loc[ppDirections['direction']==x])
            count = len(ppDirections.iloc[:,1].loc[ppDirections['direction']==x])
            tot = len(ppDirections.iloc[:,1])
            percTocchiPPDir = count / tot * 100
            #print("var pp: "+str(varTethaPPDir))
            #print("perc pp: "+str(percTocchiPPDir))
            percIndice = linea+'PercTocchiPPDir'+str(x)
            percTocchiPPDirS = percTocchiPPDirS.append(pd.Series([percTocchiPPDir], index=[percIndice]))
            varIndice = linea+'VarTethaPPDir'+str(x)
            varTethaPPDirS = varTethaPPDirS.append(pd.Series([varTethaPPDir], index=[varIndice]))
            
            varTethaSPDir = np.var(spDirections.iloc[:,0].loc[spDirections['direction']==x])
            count = len(spDirections.iloc[:,1].loc[spDirections['direction']==x])
            tot = len(spDirections.iloc[:,1])
            percTocchiSPDir = count / tot * 100
            #print("var sp: "+str(varTethaSPDir))
            #print("perc sp: "+str(percTocchiSPDir))
            percIndice = linea+'PercTocchiSPDir'+str(x)
            percTocchiSPDirS = percTocchiSPDirS.append(pd.Series([percTocchiSPDir], index=[percIndice]))
            varIndice = linea+'VarTethaSPDir'+str(x)
            varTethaSPDirS = varTethaSPDirS.append(pd.Series([varTethaSPDir], index=[varIndice]))
            
            varTethaEPDir = np.var(epDirections.iloc[:,0].loc[epDirections['direction']==x])
            count = len(epDirections.iloc[:,1].loc[epDirections['direction']==x])
            tot = len(epDirections.iloc[:,1])
            percTocchiEPDir = count / tot * 100
            #print("var ep: "+ str(varTethaEPDir))
            #print("perc ep: "+str(percTocchiEPDir))
            percIndice = linea+'PercTocchiEPDir'+str(x)
            percTocchiEPDirS = percTocchiEPDirS.append(pd.Series([percTocchiEPDir], index=[percIndice]))
            varIndice = linea+'VarTethaEPDir'+str(x)
            varTethaEPDirS = varTethaEPDirS.append(pd.Series([varTethaEPDir], index=[varIndice]))
            """
            print("Risultati: "+str(x))
            print("var pp: "+str(varTethaPPDir))
            print("perc pp: "+str(percTocchiPPDir))
            print("var sp: "+str(varTethaSPDir))
            print("perc sp: "+str(percTocchiSPDir))
            print("var ep: "+ str(varTethaEPDir))
            print("perc ep: "+str(percTocchiEPDir))
            """

        varTethaAssiDF = varTethaAssiDF.append(pd.DataFrame([[varTethaAsseX, varTethaAsseY]], columns=varTethaAssiDF.columns), ignore_index=True, sort=False)
        
        generalFeatures = generalFeatures.append(pd.DataFrame([[distanza,speed,devLinea,varPressione,varSize,dirLinea]], columns=generalFeatures.columns), ignore_index=True, sort=False)
        
        percTocchiPPDirDF = percTocchiPPDirDF.append(percTocchiPPDirS, ignore_index=True, sort=False)
        varTethaPPDirDF = varTethaPPDirDF.append(varTethaPPDirS, ignore_index=True, sort=False)

        percTocchiSPDirDF = percTocchiSPDirDF.append(percTocchiSPDirS, ignore_index=True, sort=False)
        varTethaSPDirDF = varTethaSPDirDF.append(varTethaSPDirS, ignore_index=True, sort=False)
        
        percTocchiEPDirDF = percTocchiEPDirDF.append(percTocchiEPDirS, ignore_index=True, sort=False)
        varTethaEPDirDF = varTethaEPDirDF.append(varTethaEPDirS, ignore_index=True, sort=False)
        
        #lineaNumero += 1
        #print("Risultati")
        #print(str(distanza)+", "+str(speed)+", "+str(devLinea)+", "+str(varPressione)+", "+str(varSize)+", "+str(varTethaAsseX)+", "+str(varTethaAsseY))
        #print("-----")
        #input("wait..")
        #finalDF = pd.concat([finalDF, tempFinalDF])
        tempFinalDF = pd.concat([generalFeatures,percTocchiPPDirDF,varTethaPPDirDF,percTocchiSPDirDF,varTethaSPDirDF,percTocchiEPDirDF,varTethaEPDirDF,varTethaAssiDF], axis=1)
        finalDF = finalDF.append(tempFinalDF, ignore_index=True, sort=False)
        #print(pd.concat([generalFeatures,percTocchiPPDirDF,varTethaPPDirDF,percTocchiSPDirDF,varTethaSPDirDF,percTocchiEPDirDF,varTethaEPDirDF,varTethaAssiDF], axis=1))

    #print("finalDF")
    #print(finalDF)
    return finalDF
#calcola le features sui sensori, deprecata
def calculateSensorsFeatures(data, sensors):
    returns = pd.Series([])
    for sensor in sensors:
        subDataSensor = data.loc[data[0] == str(sensor)]
        matricola = data.iloc[1][5]
        subDataSensor = subDataSensor.dropna(axis='columns')
        #subDataSensor = subDataSensor.loc[:,(subDataSensor != 0).any(axis=0)]
        numCol = len(subDataSensor.columns)
        numRows = len(subDataSensor.index)    
        intervalArray = [20, 50, 80, 100]
        percentageProgress = []   
        for value in intervalArray:
            temp = round((numRows/100)*value)
            percentageProgress.append(temp)
        if(sensor == 'actions'):
            numCol = numCol - 1
        for eachCol in range(1,numCol-1):
            subDataSensorColumn = pd.Series([])
            subDataSensorColumn = subDataSensor[subDataSensor.columns[eachCol]].astype('float64')
            for eachPercentage in percentageProgress:
                if(eachPercentage != 0):
                    if(np.nanmean(subDataSensorColumn[0:eachPercentage])==matricola and np.nanmean(subDataSensorColumn[0:eachPercentage]) != float(1)):
                        print("ATTENZIONE: CALCOLO FTRS SU MTR")
                    else:
                        returns = returns.append(pd.Series([np.nanmean(subDataSensorColumn[0:eachPercentage])]), ignore_index=True)
                else:
                    returns = returns.append(pd.Series([0]), ignore_index=True)
    return [returns]
"""
estrae i dati del pattern (madeWith, patternType, userData)
"""
def extractPathUserData(data, info):
    returns = pd.Series([])
    patternType = pd.Series([])
    madeWith = pd.Series([])
    userData = pd.Series([])
    for eachInfo in info:
        subDataInfo = data.loc[data[0] == eachInfo]
        subDataInfo = subDataInfo.dropna(axis='columns')
        subDataInfo = subDataInfo.reset_index(drop=True)
        if(eachInfo == 'patternType'):
            patternType = patternType.append(pd.Series(subDataInfo.iloc[0][1], index=['TipoPattern']))
            patternType = patternType.append(pd.Series(subDataInfo.iloc[0][2], index=['DiffRisc']))
        elif(eachInfo == 'madeWith'):
            madeWith = madeWith.append(pd.Series(subDataInfo.iloc[0][1], index=['Mano']))
            madeWith = madeWith.append(pd.Series(subDataInfo.iloc[0][2], index=['Dito']))
        elif(eachInfo == 'userData'):
           userData = userData.append(pd.Series(subDataInfo.iloc[0][1], index=['Matricola']))
           userData = userData.append(pd.Series(subDataInfo.iloc[0][2], index=['Eta']))
           userData = userData.append(pd.Series(subDataInfo.iloc[0][3], index=['Sesso']))
    """
    print(userData)
    print("------")
    print(madeWith)
    print("------")
    print(patternType)
    print("------")
    """
    returns = returns.append(userData)
    returns = returns.append(patternType)
    returns = returns.append(madeWith)
    return returns

