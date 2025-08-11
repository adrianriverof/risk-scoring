#!/usr/bin/env python
# coding: utf-8

# # Retraining Code

# In[2]:


#1.LIBRARIES

import numpy as np
import pandas as pd
import pickle

from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import Binarizer
from sklearn.preprocessing import MinMaxScaler

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingRegressor

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline


#2.LOAD DATA

path = '../../02_Data/01_Originals/loans.csv'
df = pd.read_csv(path, index_col = 0)


#3.VARIABLES AND FINAL ENTRIES
final_variables = ['verified_income',
                  'housing',
                  'purpose',
                  'num_installments',
                  'employment_duration',
                  'rating',
                  'income',
                  'dti',
                  'num_credit_lines',
                  'pct_revolving_utilization',
                  'principal',
                  'interest_rate',
                  'installment_amount',
                  'num_derogatories',
                  'status',
                  'amount_amortized',
                  'amount_recovered']

to_delete = df.loc[df.income > 300000].index.values
df = df[~df.index.isin(to_delete)]
df = df[final_variables]


#4.SUPPORT FUNCTIONS

def data_quality(temp):
    temp['employment_duration'] = temp['employment_duration'].fillna('unknown')
    for column in temp.select_dtypes('number').columns:
        temp[column] = temp[column].fillna(0)
    return temp

def variable_creation_pd(df):
    
    temp = df.copy()
    
    temp['target_pd'] = np.where(temp.status.isin(['Charged Off','Does not meet the credit policy. Status:Charged Off','Default']), 1, 0)
    
    temp.housing = temp.housing.replace(['ANY','NONE','OTHER'],'MORTGAGE')
    
    temp.purpose = temp.purpose.replace(['wedding','educational','renewable_energy'],'other')
    

    temp.drop(columns = ['status','amount_amortized','amount_recovered'],inplace = True)
    
    temp_x = temp.iloc[:,:-1]
    temp_y = temp.iloc[:,-1]
    
    return(temp_x,temp_y)

def variable_creation_ead(df):
    
    temp = df.copy()
    
    temp['remaining'] = temp.principal - temp.amount_amortized
    
    temp['target_ead'] = temp.remaining / temp.principal
    
    temp.housing = temp.housing.replace(['ANY','NONE','OTHER'],'MORTGAGE')
    
    temp.purpose = temp.purpose.replace(['wedding','educational','renewable_energy'],'other')
    
    temp.drop(columns = ['status','amount_amortized','amount_recovered','remaining'],inplace = True)
    
    temp_x = temp.iloc[:,:-1]
    temp_y = temp.iloc[:,-1]
    
    return(temp_x,temp_y)

def variable_creation_lgd(df):
    
    temp = df.copy()
    
    temp['remaining'] = temp.principal - temp.amount_amortized
    
    temp['target_lgd'] = 1 - (temp.amount_recovered / temp.remaining)
    
    temp['target_lgd'] = temp['target_lgd'].fillna(0)
    
    temp.housing = temp.housing.replace(['ANY','NONE','OTHER'],'MORTGAGE')
    
    temp.purpose = temp.purpose.replace(['wedding','educational','renewable_energy'],'other')
    
    temp.drop(columns = ['status','amount_amortized','amount_recovered','remaining'],inplace = True)
    
    temp_x = temp.iloc[:,:-1]
    temp_y = temp.iloc[:,-1]
    
    return(temp_x,temp_y)



#5.QUALITY AND VARIABLE CREATION
x_pd, y_pd = variable_creation_pd(data_quality(df))
x_ead, y_ead = variable_creation_ead(data_quality(df))
x_lgd, y_lgd = variable_creation_lgd(data_quality(df))


#6.LOAD TRAINING PIPES
pipe_training_pd_path  = '../../04_Models/pipe_training_pd.pickle'
pipe_training_ead_path = '../../04_Models/pipe_training_ead.pickle'
pipe_training_lgd_path = '../../04_Models/pipe_training_lgd.pickle'


with open(pipe_training_pd_path, mode='rb') as file:
   pipe_training_pd = pickle.load(file)

with open(pipe_training_ead_path, mode='rb') as file:
   pipe_training_ead = pickle.load(file)

with open(pipe_training_lgd_path, mode='rb') as file:
   pipe_training_lgd = pickle.load(file)


#7.TRAINING
pipe_execution_pd  = pipe_training_pd.fit(x_pd,y_pd)
pipe_execution_ead = pipe_training_ead.fit(x_ead,y_ead)
pipe_execution_lgd = pipe_training_lgd.fit(x_lgd,y_lgd)


#8.SAVE TRAINED MODELS IN EXECUTION PIPE
path_pipe_execution_pd  = '../../04_Models/pipe_execution_pd.pickle'
path_pipe_execution_ead = '../../04_Models/pipe_execution_ead.pickle'
path_pipe_execution_lgd = '../../04_Models/pipe_execution_lgd.pickle'

with open(path_pipe_execution_pd, mode='wb') as file:
   pickle.dump(pipe_execution_pd, file)

with open(path_pipe_execution_ead, mode='wb') as file:
   pickle.dump(pipe_execution_ead, file)

with open(path_pipe_execution_lgd, mode='wb') as file:
   pickle.dump(pipe_execution_lgd, file)

