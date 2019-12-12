# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 16:34:55 2019

@author: robby
"""
import pandas as pd


def getStressClass(stressLevel):
    if 0 <= stressLevel <= 9:
        return 'Normal'
    elif 10 <= stressLevel <= 13:
        return 'Mild'
    elif 14 <= stressLevel <= 20:
        return 'Moderate'
    elif 21 <= stressLevel <= 27:
        return 'Severe'
    else:
        return 'Extremely Severe'


def getAnsiaClass(ansiaLevel):
    if 0 <= ansiaLevel <= 7:
        return 'Normal'
    elif 8 <= ansiaLevel <= 9:
        return 'Mild'
    elif 10 <= ansiaLevel <= 14:
        return 'Moderate'
    elif 15 <= ansiaLevel <= 19:
        return 'Severe'
    else:
        return 'Extremely Severe'


def getDepressioneClass(depressioneLevel):
    if 0 <= depressioneLevel <= 14:
        return 'Normal'
    elif 15 <= depressioneLevel <= 18:
        return 'Mild'
    elif 19 <= depressioneLevel <= 25:
        return 'Moderate'
    elif 26 <= depressioneLevel <= 33:
        return 'Severe'
    else:
        return 'Extremely Severe'


def calculateSurveyResults():
    rawDataPath = 'C:/Users/nmacchiarulo/PycharmProjects/EmoTouch_Analysis/data/results/'
    dass42File = rawDataPath+'Questionario DASS-42 (Risposte)_new.xlsx'
    
    # stress: 1, 6, 8, 11, 12, 14, 18, 22, 27, 29, 32, 33, 35, 39, 
    # ansia: 2, 4, 7, 9, 15, 19, 20, 23, 25, 28, 30, 36, 40, 41, 
    # depressione: 3, 5, 10, 13, 16, 17, 21, 24, 26, 31, 34, 37, 38, 42 
    # rispetto alle colonne (si parte da 0..) del df: colonna 2-domanda1, colonna3-domanda2 etc..
    
    data = pd.read_excel(dass42File, sheet_name="Risposte del modulo 1")
    #print (data.iloc[0])
    
    stressArray = [1, 6, 8, 11, 12, 14, 18, 22, 27, 29, 32, 33, 35, 39]
    ansiaArray = [2, 4, 7, 9, 15, 19, 20, 23, 25, 28, 30, 36, 40, 41]
    depressioneArray = [3, 5, 10, 13, 16, 17, 21, 24, 26, 31, 34, 37, 38, 42]
    
    finalResults = pd.DataFrame(columns=['Matricola','Data','StressLevel','AnsiaLevel','DepressionLevel'])
    
    pd.set_option('display.max_columns',8)#righe max_rows
    
    for x in range(0, len(data.index)):
        stressTot = 0
        ansiaTot = 0
        depressioneTot = 0
        row = data.iloc[x]
        
        #print(row[0])
        #if(row[1] == 649923 or row[1]== 653341 or row[1]==653442):
        #    print("ECCOLOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        #print(row[1])
        
        for stressElement in stressArray:
            stressTot += row[stressElement+1]
    
        for ansiaElement in ansiaArray:
            ansiaTot += row[ansiaElement+1]
    
        for depressioneElement in depressioneArray:
            depressioneTot += row[depressioneElement+1]
        """
        print("Risultati")
        print(stressTot)
        print(ansiaTot)
        print(depressioneTot)
        """
        #stressLevel = getStressClass(stressTot)
        #ansiaLevel = getAnsiaClass(ansiaTot)
        #depressioneLevel = getDepressioneClass(depressioneTot)
        finalResults = finalResults.append(pd.DataFrame([[row[1], row[0], stressTot, ansiaTot, depressioneTot]], columns=finalResults.columns), sort=False, ignore_index=True)
    
    finalResults.to_excel(rawDataPath+'risultatiQuestionario_numerici.xlsx', sheet_name='DAS',index=False)
    return finalResults
    #print(finalResults)


def calculateSurveyClassResults():
    rawDataPath = 'C:/Users/nmacchiarulo/PycharmProjects/EmoTouch_Analysis/data/results/'
    dass42File = rawDataPath + 'Questionario DASS-42 (Risposte)_new.xlsx'

    # stress: 1, 6, 8, 11, 12, 14, 18, 22, 27, 29, 32, 33, 35, 39,
    # ansia: 2, 4, 7, 9, 15, 19, 20, 23, 25, 28, 30, 36, 40, 41,
    # depressione: 3, 5, 10, 13, 16, 17, 21, 24, 26, 31, 34, 37, 38, 42
    # rispetto alle colonne (si parte da 0..) del df: colonna 2-domanda1, colonna3-domanda2 etc..

    data = pd.read_excel(dass42File, sheet_name="Risposte del modulo 1")
    # print (data.iloc[0])

    stressArray = [1, 6, 8, 11, 12, 14, 18, 22, 27, 29, 32, 33, 35, 39]
    ansiaArray = [2, 4, 7, 9, 15, 19, 20, 23, 25, 28, 30, 36, 40, 41]
    depressioneArray = [3, 5, 10, 13, 16, 17, 21, 24, 26, 31, 34, 37, 38, 42]

    finalResults = pd.DataFrame(columns=['Matricola', 'Data', 'StressLevel', 'AnsiaLevel', 'DepressionLevel'])

    pd.set_option('display.max_columns', 8)  # righe max_rows

    for x in range(0, len(data.index)):
        stressTot = 0
        ansiaTot = 0
        depressioneTot = 0
        row = data.iloc[x]

        # print(row[0])
        # if(row[1] == 649923 or row[1]== 653341 or row[1]==653442):
        #    print("ECCOLOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        # print(row[1])

        for stressElement in stressArray:
            stressTot += row[stressElement + 1]

        for ansiaElement in ansiaArray:
            ansiaTot += row[ansiaElement + 1]

        for depressioneElement in depressioneArray:
            depressioneTot += row[depressioneElement + 1]
        """
        print("Risultati")
        print(stressTot)
        print(ansiaTot)
        print(depressioneTot)
        """
        stressLevel = getStressClass(stressTot)
        ansiaLevel = getAnsiaClass(ansiaTot)
        depressioneLevel = getDepressioneClass(depressioneTot)
        finalResults = finalResults.append(
            pd.DataFrame([[row[1], row[0], stressLevel, ansiaLevel, depressioneLevel]], columns=finalResults.columns),
            sort=False, ignore_index=True)

    finalResults.to_excel(rawDataPath + 'risultatiQuestionario.xlsx', sheet_name='DAS', index=False)
    return finalResults
    # print(finalResults)


def getSurveyResults():
    rawDataPath = 'C:/Users/nmacchiarulo/PycharmProjects/EmoTouch_Analysis/data/results/'
    finalResults = pd.read_excel(rawDataPath+'risultatiQuestionario_numerici.xlsx', sheet_name='DAS',index=False)
    return finalResults

def getSurveyClassResults():
    rawDataPath = 'C:/Users/nmacchiarulo/PycharmProjects/EmoTouch_Analysis/data/results/'
    finalResults = pd.read_excel(rawDataPath+'risultatiQuestionario.xlsx', sheet_name='DAS',index=False)
    return finalResults

calculateSurveyResults()
calculateSurveyClassResults()