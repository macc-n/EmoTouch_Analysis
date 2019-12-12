# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 11:19:27 2019

@author: robby
"""

import numpy as np
import openpyxl
import BaseFunctions as bf
import pandas as pd
import math
import time
import BaseFunctions as bf
from sklearn.model_selection import train_test_split
from sklearn import svm
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

pd.set_option('display.max_columns',100)#righe max_rows
pd.set_option('display.max_rows',100)
#dataset = 'C:/Tesi/Applicazioni/Dataset_EmoTouchLock/Release_DS/03.06.2019-20.50/dataset_bilanciati_stress_numerico/dirLineaTask/dirLineaTask184_samples.xlsx'
dataset = 'C:/Tesi/Applicazioni/Dataset_EmoTouchLock/Dataset_Univoco/finalDataset_10tentativi_fix.xlsx'
dataset = pd.read_excel(dataset, sheet_name='data')
dataset = dataset.fillna(0)

target_names = dataset.iloc[:,0].drop_duplicates(keep='first').astype('int64')
#print(target_names)
"""
['Extremely_Severe_Ansia','Severe_Ansia','Moderate_Ansia','Mild_Ansia','Normal_Ansia',
                'Extremely_Severe_Stress','Severe_Stress','Moderate_Stress','Mild_Stress','Normal_Stress',
                'Extremely_Severe_Depressione','Severe_Depressione','Moderate_Depressione','Mild_Depressione','Normal_Depressione']
"""
n_classes = target_names.shape[0]

#print(dataset)

y = dataset.iloc[:,0]
score = []
dataset = dataset.drop(columns = ['StressLevel','AnsiaLevel','DepressionLevel','DiffRisc','Sesso','Eta','TipoPattern','Mano','Dito'])
df = pd.DataFrame([])
idx = -len(target_names)
wb = openpyxl.Workbook()
for target in target_names:
    print(target)
    
    for x in range (0, 10):
        X_train, X_test, y_train, y_test = bf.train_test_split_custom(dataset, y, test_size=0.1, sampleNumber=x, leaveOneOut=True)

        """ con train_test_split_custom faccio già ritornare dei dataframe, 
            queste istruzioni servono solo per lo split standard
            
        X_train_ds, X_test_ds, y_train_ds, y_test_ds= train_test_split(dataset, y, test_size=0.25)
        X_train = pd.DataFrame(X_train_ds, columns=dataset.columns)
        X_test = pd.DataFrame(X_test_ds, columns=dataset.columns)
        y_train = pd.DataFrame(y_train_ds, columns=['Matricola'])
        y_test = pd.DataFrame(y_test_ds, columns=['Matricola']) 
        """
        #codice per bilanciare n pattern genuini e n non genuini
        
        X_train.loc[X_train['Matricola'] != target, 'Matricola'] = idx
        X_test.loc[X_test['Matricola'] != target, 'Matricola'] = idx
        y_train.loc[y_train['Matricola'] != target, 'Matricola'] = idx
        y_test.loc[y_test['Matricola'] != target, 'Matricola'] = idx
        """
        X_train_correct_balanced = X_train[X_train['Matricola']==target]
        X_train_incorrect_balanced = X_train[X_train['Matricola']==idx]
        y_train_correct_balanced = y_train[y_train['Matricola']==target]
        y_train_incorrect_balanced = y_train[y_train['Matricola']==idx]
        
        X_test_correct_balanced = X_test[X_test['Matricola']==target]
        X_test_incorrect_balanced = X_test[X_test['Matricola']==idx]
        y_test_correct_balanced = y_test[y_test['Matricola']==target]
        y_test_incorrect_balanced = y_test[y_test['Matricola']==idx]
        
        X_train_toUse = X_train_correct_balanced.append(X_train_incorrect_balanced.iloc[0:len(X_train_correct_balanced.index)]).drop(columns=['Matricola','Task']).reset_index(drop=True)
        X_test_toUse = X_test_correct_balanced.append(X_test_incorrect_balanced.iloc[0:len(X_test_correct_balanced.index)]).drop(columns=['Matricola']).reset_index(drop=True)
        #print(X_test_toUse.columns)
        X_test_task_direction = pd.concat([X_test_toUse['Task'], X_test_toUse['Linea1_DirLinea']], axis=1)
        #print(X_test_task_direction)
        X_test_toUse = X_test_toUse.drop(columns=['Task'])
        #print(X_test_task)
        y_train_toUse = y_train_correct_balanced.append(y_train_incorrect_balanced.iloc[0:len(y_train_correct_balanced.index)]).reset_index(drop=True)
        y_test_toUse = y_test_correct_balanced.append(y_test_incorrect_balanced.iloc[0:len(y_test_correct_balanced.index)]).reset_index(drop=True)
        """
        
        #QUI
        numTrainCorrect = len(X_train[X_train['Matricola']==target]['Task'].drop_duplicates(keep='first').index)
        #print(numTrainCorrect)
        taskTrainIncorrect = pd.Series(list(X_train[X_train['Matricola']!=target]['Task'].drop_duplicates(keep='first')))

        listaTaskTrainIncorrect = taskTrainIncorrect[taskTrainIncorrect.str.contains("difficile")].sample(math.ceil(numTrainCorrect/3))
        listaTaskTrainIncorrect = listaTaskTrainIncorrect.append(taskTrainIncorrect[taskTrainIncorrect.str.contains("facile")].sample(math.ceil(numTrainCorrect/3)))
        listaTaskTrainIncorrect = listaTaskTrainIncorrect.append(taskTrainIncorrect[taskTrainIncorrect.str.contains("medio")].sample(math.ceil(numTrainCorrect/3)))

        X_train_toUse = X_train[X_train['Matricola']==target]
        for task in listaTaskTrainIncorrect:
            X_train_toUse = pd.concat([X_train_toUse, X_train[X_train['Task']==task]])

        numTestCorrect = len(X_test[X_test['Matricola']==target]['Task'].drop_duplicates(keep='first').index)

        taskTestIncorrect = pd.Series(list(X_test[X_test['Matricola']!=target]['Task'].drop_duplicates(keep='first')))

        listaTaskTestIncorrect = taskTestIncorrect[taskTestIncorrect.str.contains("difficile")].sample(math.ceil(numTestCorrect/3))
        listaTaskTestIncorrect = listaTaskTestIncorrect.append(taskTestIncorrect[taskTestIncorrect.str.contains("facile")].sample(math.ceil(numTestCorrect/3)))
        listaTaskTestIncorrect = listaTaskTestIncorrect.append(taskTestIncorrect[taskTestIncorrect.str.contains("medio")].sample(math.ceil(numTestCorrect/3)))

        X_test_toUse = X_test[X_test['Matricola']==target]
        for task in listaTaskTestIncorrect:
            X_test_toUse = pd.concat([X_test_toUse, X_test[X_test['Task']==task]])

        #taskTrainIncorrectNum = taskTrainIncorrect.sample(numTrainCorrect)
        X_test_task_direction = pd.concat([X_test_toUse['Task'], X_test_toUse['Linea1_DirLinea']], axis=1).reset_index(drop=True)

        #QUI è possibile effettuare dei test con soli pattern facili
        """
        X_train_toUse = X_train_toUse[X_train_toUse['Task'].str.contains("_facile_")==False]
        X_test_toUse = X_test_toUse[X_test_toUse['Task'].str.contains("_medio_")==False]
        X_test_toUse = X_test_toUse[X_test_toUse['Task'].str.contains("_difficile_")==False]
        """
        #QUI
        X_test_task_direction = pd.concat([X_test_toUse['Task'], X_test_toUse['Linea1_DirLinea']], axis=1).reset_index(drop=True)
        
        
        y_train_toUse = X_train_toUse.loc[X_train_toUse.index][['Matricola']].reset_index(drop=True)
        #y_train_toUse= y_train_toUse[['Matricola']]
        y_test_toUse = X_test_toUse.loc[X_test_toUse.index][['Matricola']].reset_index(drop=True)

        X_train_toUse = X_train_toUse.drop(columns=['Task','Matricola']).reset_index(drop=True)
        X_test_toUse = X_test_toUse.drop(columns=['Task','Matricola']).reset_index(drop=True)
        
        #QUI
        n_components = 57
        """
        clf = svm.SVC(gamma='auto')
        
        pca = PCA(n_components=n_components, svd_solver='randomized',
                  whiten=True).fit(X_train_toUse)
        
        X_train_pca = pca.transform(X_train_toUse)
        X_test_pca = pca.transform(X_test_toUse)
        
        param_grid = {'C': [1e3, 5e3, 1e4, 5e4, 1e6],
                      'gamma': [0.0000001, 0.0005, 0.001, 0.005, 0.01, 0.1], }
        #GridSearchCV(SVC(kernel='rbf', class_weight='balanced', probability=True), param_grid, cv=5, iid=False)
        #clf = GridSearchCV(SVC(kernel='rbf', class_weight='balanced', probability=True), param_grid, cv=5, iid=False)
        """
        clf = RandomForestClassifier(n_estimators=100)
        
        clf = clf.fit(X_train_toUse, y_train_toUse.values.ravel())
        
        y_pred = clf.predict(X_test_toUse)
        y_pred_proba = clf.predict_proba(X_test_toUse)
       
        predicted = pd.DataFrame(y_pred, columns=['predetto_'+str(idx)])
        predicted_proba = pd.DataFrame(y_pred_proba, columns=clf.classes_)
        #print(predicted_proba)
        df = pd.concat([X_test_task_direction, y_test_toUse, predicted_proba, predicted], axis=1)
        #print(df)
        #time.sleep(120)
        bf.append_df_to_excel('C:/Tesi/Applicazioni/Dataset_EmoTouchLock/VerificationDatasets/10tentativi/'+str(target)+'.xlsx', df.drop(columns=[idx]), sheet_name="tentativo_"+str(x))
        score.append(accuracy_score(y_test_toUse, y_pred))
        idx += 1
        
    print(np.mean(score))
    score.clear()
