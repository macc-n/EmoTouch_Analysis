# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 17:16:11 2019

@author: robby
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 11:19:27 2019

@author: robby
"""

import numpy as np
import time
import BaseFunctions as bf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import  svm
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier

"""
qui si calcola l'accuratessa con random forest. per l'svm è opportuno passare i _pca del train/test
"""

dataset = 'C:/Tesi/Applicazioni/Dataset_EmoTouchLock/Dataset_Univoco/finalDataset_10tentativi_fix.xlsx'
#dataset = 'C:/Tesi/Applicazioni/Dataset_EmoTouchLock/Release_DS/03.06.2019-20.50/dataset_bilanciati_stress_numerico/dirLineaTask/dirLineaTask184_samples.xlsx'

dataset = pd.read_excel(dataset, sheet_name='data')
dataset = dataset.fillna(0)

#daEliminare = [50222, 656488, 661458, 663297, 683892]
for da in daEliminare:
    dataset = dataset[dataset['Matricola']!=da]
target_names = dataset.iloc[:,0].drop_duplicates(keep='first').astype('str')
#print("auto-custom 0.1 pca")
"""
['Extremely_Severe_Ansia','Severe_Ansia','Moderate_Ansia','Mild_Ansia','Normal_Ansia',
                'Extremely_Severe_Stress','Severe_Stress','Moderate_Stress','Mild_Stress','Normal_Stress',
                'Extremely_Severe_Depressione','Severe_Depressione','Moderate_Depressione','Mild_Depressione','Normal_Depressione']
"""
n_classes = target_names.shape[0]

#print(dataset)

y = dataset.iloc[:,0]
score=[]
dataset = dataset.drop(columns = ['StressLevel','AnsiaLevel','DepressionLevel','TipoPattern','DiffRisc','Mano','Dito','Eta'])
df = pd.DataFrame([])
idx = -len(target_names)
#for target in target_names:
for x in range (0, 10):
    print(x)
    X_train, X_test, y_train, y_test = bf.train_test_split_custom(dataset, y, test_size=0.05, sampleNumber=x, leaveOneOut=True)
    
    X_train = X_train.drop(columns=['Task','Matricola'])
    X_test  = X_test.drop(columns=['Task','Matricola']) 
    #print(X_train.index)
    #print(X_test.index)
    n_components = 57
    #scale
    clf = svm.SVC(gamma='scale')
    
    pca = PCA(n_components=n_components, svd_solver='randomized',
              whiten=True).fit(X_train)
    
    X_train_pca = pca.transform(X_train)
    X_test_pca = pca.transform(X_test)
    
    param_grid = {'C': [1e6, 1e3, 5e3, 1e4, 5e4],
                  'gamma': [0.0000001, 0.0005, 0.001, 0.005, 0.01, 0.1], }
    #GridSearchCV(SVC(kernel='rbf', class_weight='balanced', probability=True), param_grid, cv=5, iid=False)
    #clf = GridSearchCV(SVC(kernel='rbf', class_weight='balanced', probability=True), param_grid, cv=5, iid=False)
    clf = RandomForestClassifier(n_estimators=100)
    clf = clf.fit(X_train, y_train.values.ravel())
    
    y_pred = clf.predict(X_test)
    y_pred_proba = clf.predict_proba(X_test)
    #print(classification_report(y_test_toUse.values.ravel(), y_pred, target_names=target_names))
    #print(y_test_toUse.values.ravel())
    #print(y_pred)
    #matricola = pd.DataFrame(y_test_toUse, columns=y_test_toUse.columns)
    #matricola = matricola[matricola['Matricola']!=0]
    predicted = pd.DataFrame(y_pred, columns=['predetto_'+str(idx)])
    predicted = predicted.reset_index(drop=True)
    predicted_proba = pd.DataFrame(y_pred_proba, columns=clf.classes_)
    predicted_proba = predicted_proba.reset_index(drop=True)
    #df = pd.concat([df, y_test_toUse.reset_index(drop=True), predicted, predicted_proba], axis=1)
    #df = df.append(result, ignore_index=True, sort=False)
    scr = accuracy_score(y_test, y_pred)
    print(scr)
    #print(classification_report(y_test, y_pred, target_names=target_names))
    score.append(scr)
    idx += 1
    #print(df)
    #input("wait..")
#print(df)
print(np.mean(score))
#print(target_names)
#print(confusion_matrix(y_test, y_pred, labels=range(n_classes)))