# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 16:42:22 2019

@author: robby
"""
import pandas as pd

#Serve per avere dei dataset bilanciati in base al numero di swipe.

def rebalanceDataset(dataset, sampleNumber, minRows = 0):
    listaMatricole = dataset['Matricola']
    listaMatricole = listaMatricole.drop_duplicates(keep='first')
    print(listaMatricole)
    
    balancedDataset = pd.DataFrame(columns = dataset.columns)
    
    for matricola in listaMatricole:
        if len(dataset[dataset['Matricola']==matricola]) >= minRows:
            balancedDataset = balancedDataset.append(dataset[dataset['Matricola']==matricola].sample(n=sampleNumber), ignore_index=True, sort=False)
        
    return balancedDataset
#No ZScore
#datasetName = 'C:/Tesi/Applicazioni/Dataset_EmoTouchLock/Release_DS/03.06.2019-20.50/dataset_almeno10_per_linee_plus_stress_noZscore/finalDataset_1row_each_line_plus_stress.xlsx'
#Si ZScore
datasetName = 'C:/Tesi/Applicazioni/Dataset_EmoTouchLock/Dataset_Univoco/finalDataset_6tentativi_fix.xlsx'

dataset = pd.read_excel(datasetName, sheet_name='data')


#dataset_36samples = rebalanceDataset(dataset, 36, 36)
dataset_72samples = rebalanceDataset(dataset, 72, 72)
#dataset_120samples = rebalanceDataset(dataset, 120, 120)
#dataset_184samples = rebalanceDataset(dataset, 184, 184)

path = "C:/Tesi/Applicazioni/Dataset_EmoTouchLock/Dataset_Univoco/finalDataset_6tentativi__fix_"
path = path.replace("\\","/")

#dataset_36samples.to_excel(path+"36_samples.xlsx", sheet_name='data', index=False)
#dataset_36samples.to_csv(path+"36_samples.csv", sep=',',na_rep = '0', index=False)

dataset_72samples.to_excel(path+"72_samples.xlsx", sheet_name='data', index=False)
dataset_72samples.to_csv(path+"72_samples.csv", sep=',',na_rep = '0', index=False)

#dataset_120samples.to_excel(path+"120_samples.xlsx", sheet_name='data', index=False)
#dataset_120samples.to_csv(path+"120_samples.csv", sep=',',na_rep = '0', index=False)

#dataset_184samples.to_excel(path+"184_samples.xlsx", sheet_name='data', index=False)
#dataset_184samples.to_csv(path+"184_samples.csv", sep=',',na_rep = '0', index=False)