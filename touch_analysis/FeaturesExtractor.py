# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 20:11:37 2019

@author: robby
"""

import numpy as np
from scipy import stats
import pandas as pd
import openpyxl as opx
import os
import datetime
import SppFunFtrsExt as supp
import time
import math
import AnglePointsExtractor as ape
import BaseFunctions as bf
import DASS42Extractor as questions
from matplotlib.backends.backend_pdf import PdfPages

#pd.set_option("display.max_rows",500)
"""
metodo per calcolare le features, ma lo farà chiamando funzioni in altre librerie (per comodità)
"""
def calculateFeatures(fileName, survey):
    print(fileName)
    #print("survey")
    #print(survey)
    
    """
    si leggono i dati raw per poi eseguire delle operazioni di pulizia quali drop di duplicati, reset dell'index etc.
    """
    
    results = pd.DataFrame([])
    data = pd.read_excel(fileName, sheet_name="correct", header=None)
    matrName = os.path.basename(os.path.dirname(os.path.dirname(fileName)))
    folderName = os.path.basename(os.path.dirname(fileName))
    fileNumber = int(os.path.splitext(os.path.basename(fileName))[0])
    if(data.empty == False):
        
        actionsInfo = data.loc[data[0] == "actions"]
        actionsInfo = actionsInfo.dropna(axis='columns')
        actionsInfo = actionsInfo.drop_duplicates(subset=[1], keep='first')
        actionsInfo = actionsInfo.drop_duplicates(subset=[2,3], keep='first')
        actionsInfo = actionsInfo.reset_index(drop=True)
        actionsInfo = bf.aggiungiDeltaTimeTraPunti(actionsInfo)
        anglePoints = ape.getDirectionChangingPoints(actionsInfo)
        
        #calcola le features sui tocchi
        results = supp.calculateTouchFeatures(actionsInfo, anglePoints)
        
        #si leggono i dati del pattern quali diff. riscontrata, mano dito etc..
        touches = data.iloc[:,0]
        touches = touches.drop_duplicates()
        touches = touches[touches>str(99)]
        dataInfo = pd.DataFrame(columns = ['Matricola','Eta','Sesso','TipoPattern','DiffRisc','Mano','Dito','Task'])
        dataInfoSurvey = pd.DataFrame(columns = ['StressLevel','AnsiaLevel','DepressionLevel'])
        
        temp = supp.extractPathUserData(data,touches[1:len(touches.index)])
        temp2 = pd.Series(str(matrName)+"_"+folderName+"_"+str(fileNumber)+"_", index=['Task'])
        temp = temp.append(temp2)
        sup = len(results.index)
        
        for x in range (0, sup):         
            dataInfo = dataInfo.append(temp, ignore_index=True)
            #dataInfo = dataInfo.append(, ignore_index=True)
        #print("parte 1")
        #print(dataInfo)
        for x in range (0, sup):
            dataInfoSurvey = dataInfoSurvey.append(survey, ignore_index=True)
        #print("parte 2")
        #print(dataInfoSurvey)
        
        dataInfo = pd.concat([dataInfo, dataInfoSurvey], axis=1)
        #print("parte 3")
        #print(dataInfo)
        
        results = pd.concat([dataInfo, results], axis=1)
        
        #una volta concatenati vengono normalizzati con lo zscore. Le colonne riseguenti sono le colonne su cui non verrà fatta la normalizzazione
        
        cols = list(results.columns)
        cols.remove('Matricola')
        cols.remove('Eta')
        cols.remove('Sesso')
        cols.remove('TipoPattern')
        cols.remove('DiffRisc')
        cols.remove('Mano')
        cols.remove('Dito')
        cols.remove('Task')
        cols.remove('StressLevel')
        cols.remove('AnsiaLevel')
        cols.remove('DepressionLevel')
        cols.remove('Linea1_DirLinea')
        
        for idx in range(0, len(results.columns)):
            if results.iloc[:,idx].name.find("Perc") != -1:
                cols.remove(results.iloc[:,idx].name)
        
        results[cols] = results[cols].apply(stats.zscore)
        
    else:
        results = pd.DataFrame([])
        print("file senza correct")
    return [results]


featuresStd = pd.DataFrame([])
rawDataPath = 'C:/Tesi/Applicazioni/Dataset_EmoTouchLock/Dataset_Univoco/DataSet10tentativi/'
finalDatasetExcel = rawDataPath+'finalDataset_10tentativi_fix.xlsx'
finalDatasetCsv = rawDataPath+'finalDataset_10tentativi_fix.csv'
#pp = PdfPages("C:/Tesi/figureDaControllare_algoritmo_v36_1perPuntiIniFin.pdf")

inizio = datetime.datetime.now()

arrayDifficilePercorsi = []
arrayFacilePercorsi = []
arrayMedioPercorsi = []
arrayDifficileFiles = []
arrayFacileFiles = []
arrayMedioFiles = []

cpt = 0
index = 0
countSurveyResults = 0
boolTrovataMatricola = False
oldMatricola = 0
risposte = questions.getSurveyResults()
#print(risposte)
"""
prima di chiamare calculate features vengono lette le risposte ai questionari degli utenti presenti nel dataset.
"""
for root, dirs, files in os.walk(rawDataPath):   
    #input("WAIT")
    """
    print("root")
    print(root)
    print("dirs")
    print(dirs)
    print("file")
    print(files)
    """
    if len(dirs) == 3:
        #print("WE")
        #print("ROOT:"+str(root))
        matricola = os.path.basename(root)
        #print("DIR: "+str(dirs))
        #print("MTR: "+str(matricola))
        lenSurvey = len(risposte.loc[risposte['Matricola'] == int(matricola)])
        survey = risposte.loc[risposte['Matricola'] == int(matricola)]
        survey = survey.reset_index(drop=True)
        #print(survey)
        for dire in dirs:            
            if dire == 'difficile':
                #print("difficile")
                #print(len(os.listdir(os.path.join(root,dire))))
                cptDifficile = math.ceil(len(os.listdir(os.path.join(root,dire)))/lenSurvey)
            elif dire == 'facile':
                #print("facile")
                #print(len(os.listdir(os.path.join(root,dire))))
                cptFacile = math.ceil(len(os.listdir(os.path.join(root,dire)))/lenSurvey)
            elif dire == 'medio':
                #print("medio")
                #print(len(os.listdir(os.path.join(root,dire))))
                cptMedio = math.ceil(len(os.listdir(os.path.join(root,dire)))/lenSurvey)
            #cpt += len(os.listdir(os.path.join(root,dire)))
        #print("CPT:"+str(cpt))     
        """
        print("MTR: "+str(matricola))
        print("Per ogni difficolta'")
        print(cptDifficile)
        print(cptFacile)
        print(cptMedio)
        print("NUM. SURV.: "+str(len(risposte.loc[risposte['Matricola'] == int(matricola)])))
        """
        #qui con la matricola leggo i questionari svolti e faccio l'operazione di divisione per capire quanti ne devo prendere per ogni questionario
        boolTrovataMatricola = True   
    elif len(files) != 0 and boolTrovataMatricola == True:
        #print("NE")
        #print(survey)
        for file in files:
            #print("FILES: "+str(files))
            #print(os.path.join(root,file))
            if(file != 'statistiche.xlsx' and file != 'finalDataset_1row_each_line.xlsx'):
                percorso = os.path.join(root,file)
                percorso = percorso.replace('\\', '/')
                #print(percorso)
                difficulty = os.path.basename(os.path.dirname(percorso))
                #print(difficulty)
                if difficulty == 'difficile':
                    arrayDifficilePercorsi.append(file)
                    
                elif difficulty == 'facile':
                    arrayFacilePercorsi.append(file)
                    
                elif difficulty == 'medio':
                    arrayMedioPercorsi.append(file)
        #print("Ordino i file..")
        #print(root.replace('\\','/'))
        for percorso in arrayDifficilePercorsi:
            arrayDifficileFiles.append(int(os.path.splitext(percorso)[0]))
            
        for percorso in arrayFacilePercorsi:
            arrayFacileFiles.append(int(os.path.splitext(percorso)[0]))
    
        for percorso in arrayMedioPercorsi:
            arrayMedioFiles.append(int(os.path.splitext(percorso)[0]))
        
        arrayFacileFiles.sort()
        arrayMedioFiles.sort()
        arrayDifficileFiles.sort()
        
        arrayDifficilePercorsi = []
        arrayMedioPercorsi = []
        arrayFacilePercorsi = []
        
        percorso = root
        for file in arrayFacileFiles:
            arrayFacilePercorsi.append(os.path.join(percorso,str(file)+".xlsx").replace('\\','/'))
        for file in arrayMedioFiles:
            arrayMedioPercorsi.append(os.path.join(percorso,str(file)+".xlsx").replace('\\','/'))
        for file in arrayDifficileFiles:
            arrayDifficilePercorsi.append(os.path.join(percorso,str(file)+".xlsx").replace('\\','/'))
        #print(arrayDifficilePercorsi)
        #print(arrayMedioPercorsi)
        #print(arrayFacilePercorsi)
        """
        print(arrayFacileFiles)
        print(arrayMedioFiles)
        print(arrayDifficileFiles)
        """
        #time.sleep(5)

        index = 0
        for percorso in arrayDifficilePercorsi:
            #if int(matricola) == 656883:
            #print("difficile")
            #print("count: "+str(countSurveyResults))
            #print("cpt: "+str(cptDifficile))
            if (countSurveyResults >= cptDifficile):
                countSurveyResults = 0
                index += 1
            #print(os.path.split(path))
            #print("idx: "+str(index))
            featuresStd = featuresStd.append(calculateFeatures(percorso, survey.iloc[index,2:5]), ignore_index=True, sort=False)
            countSurveyResults += 1
            #time.sleep(5)
        index = 0
        countSurveyResults = 0
        arrayDifficileFiles = []
        arrayDifficilePercorsi = []
        
        for percorso in arrayMedioPercorsi:
            #if int(matricola) == 656883:
            #print("medio")
            #print("count: "+str(countSurveyResults))
            #print("cpt: "+str(cptMedio))
            if (countSurveyResults >= cptMedio):
                countSurveyResults = 0
                index += 1
            #print("idx: "+str(index))
            featuresStd = featuresStd.append(calculateFeatures(percorso, survey.iloc[index,2:5]), ignore_index=True, sort=False)
            countSurveyResults += 1
        index = 0
        countSurveyResults = 0
        arrayMedioFiles = []
        arrayMedioPercorsi = []
        
        for percorso in arrayFacilePercorsi:
            #if int(matricola) == 656883:
            #print("Facile")
            #print("count: "+str(countSurveyResults))
            #print("cpt: "+str(cptFacile))
            if (countSurveyResults >= cptFacile):
                countSurveyResults = 0
                index += 1
            #print("idx: "+str(index))
            featuresStd = featuresStd.append(calculateFeatures(percorso, survey.iloc[index,2:5]), ignore_index=True, sort=False)
            countSurveyResults += 1
        index = 0
        countSurveyResults = 0
        arrayFacileFiles = []
        arrayFacilePercorsi = []
    else:
        """
        print("qui")
        print("root")
        print(root)
        print("dirs")
        print(dirs)
        print("file")
        print(files)
        """
        boolTrovataMatricola = False
        index = 0
        countSurveyResults = 0
        arrayDifficilePercorsi = []
        arrayFacilePercorsi = []
        arrayMedioPercorsi = []
        arrayDifficileFiles = []
        arrayFacileFiles = []
        arrayMedioFiles = []
        
#pp.close()
#TODO implementa DataFrame.replace per sostituire gli indici con i valoriin stringa
fine = datetime.datetime.now()
print("Inizio: "+str(inizio))
print("Fine: "+str(fine))
featuresStd.dropna()
featuresStd.to_excel(finalDatasetExcel, sheet_name='data', index=False)
featuresStd.to_csv(finalDatasetCsv, sep=',',na_rep = '0', index=False)
            