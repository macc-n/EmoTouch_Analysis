# -*- coding: utf-8 -*-
"""
Created on Thu May 23 15:06:12 2019

@author: robby
"""
import AnglePointsExtractor as ape
import pandas as pd
import os
import BaseFunctions as bf
import numpy as np
import SppFunFtrsExt as supp
#1-facile-0
#647340-difficile-0
#654683-difficile-0

#file di test per i vari metodi. si consiglia di usarlo per testare i metodi e prendere confidenza con essi

path = "C:/Tesi/Applicazioni/Dataset_EmoTouchLock/Release_DS/03.06.2019-20.50/Extracted_DS_03_06/662644/difficile/15.xlsx"
df = pd.read_excel(path, sheet_name='correct', header=None)

actionsInfo = df.loc[df[0] == "actions"]
actionsInfo = actionsInfo.dropna(axis='columns')
actionsInfo = actionsInfo.drop_duplicates(subset=[1], keep='first')
actionsInfo = actionsInfo.drop_duplicates(subset=[2,3], keep='first')
actionsInfo = actionsInfo.reset_index(drop=True)

#disp = bf.calcolaDisplacemente(actionsInfo, 0, len(actionsInfo.index))
#print("displacement")
#print(disp)

#perc1 = bf.calcolaIntervalli(actionsInfo, np.array([20,50,80,100]))
#print("Perc1")
#print(perc1)

#perc2 = bf.calcolaIntervalli(actionsInfo, np.array([30,70,100]))
#print("Perc2")
#print(perc2)
actionsInfo = bf.aggiungiDeltaTimeTraPunti(actionsInfo)
#print("actionsInfo")
#print(actionsInfo.iloc[:,8])

#subActionsInfo = bf.getSubActionsInfo(actionsInfo,4,9)
#print("subActionsInfo")
#print(subActionsInfo)

#df = bf.anglesBetweenThreePoints(actionsInfo[[2,3,'Time','oldIndex']])
#print("df senza assi")
#print(df)
#df = bf.anglesBetweenThreePoints(actionsInfo[[2,3,'Time','oldIndex']], asse='x')
#print("df asse x")
#print(df)
#df = bf.anglesBetweenThreePoints(actionsInfo[[2,3,'Time','oldIndex']], asse='y')
#print("df asse y")
#print(df)
#print("DF")
#print(df)

difficulty = os.path.basename(os.path.dirname(path))
#if difficulty == 'facile':
points = ape.getDirectionChangingPoints(actionsInfo)
pd.set_option('display.max_rows',20)
print(points)
"""
print(bf.getDistance(
            np.array([actionsInfo.iloc[1][2],actionsInfo.iloc[0][2]]), 
            np.array([actionsInfo.iloc[1][3],actionsInfo.iloc[0][3]])))
"""
f = ape.drawPoints(actionsInfo, points, path)


#f = ape.drawPoints(actionsInfo, pd.DataFrame([]), path)
"""
rawDataPath = 'C:/Tesi/Applicazioni/Dataset_EmoTouchLock/Release_DS/03.06.2019-20.50/Extracted_DS_03_06/'
finalDataset = rawDataPath+'finalDataset_test.xlsx'

points = ape.getDirectionChangingPoints(actionsInfo)
actionsInfo = bf.aggiungiDeltaTimeTraPunti(actionsInfo)
df2 = supp.calculateTouchFeatures(actionsInfo,points)

touches = df.iloc[:,0]
touches = touches.drop_duplicates()
touches = touches[touches>str(99)]
dataInfo = pd.DataFrame(columns = ['Matricola','Eta','Sesso','TipoPattern','DiffRisc','Mano','Dito'])
temp = supp.extractPathUserData(df,touches[1:len(touches.index)])
print("Qui")
for x in range (0, len(df2.index)):         
    dataInfo = dataInfo.append(temp, ignore_index=True)
#print(df2)
#print(dataInfo)

df2 = pd.concat([dataInfo, df2], axis=1)

df2.to_excel(finalDataset, sheet_name='data', index=False)
f = ape.drawPoints(actionsInfo, points, path)
#f = ape.drawPoints(actionsInfo, points, path, inverti='no')7
"""