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


#3.SUPPORT FUNCTIONS
def data_quality(temp):
    temp['employment_duration'] = temp['employment_duration'].fillna('unknown')
    
    for column in temp.select_dtypes('number').columns:
        temp[column] = temp[column].fillna(0)
    
    return temp

def variable_creation(df):
    temp = df.copy()
    
    temp.housing = temp.housing.replace(['ANY','NONE','OTHER'],'MORTGAGE')

    temp.purpose = temp.purpose.replace(['wedding','educational','renewable_energy'],'other')

    return(temp)


def execute_models(df):
    #4.QUALITY AND VARIABLE CREATION
	x_pd  = variable_creation(data_quality(df))
	x_ead = variable_creation(data_quality(df))
	x_lgd = variable_creation(data_quality(df))


    #5.LOAD EXECUTION PIPES
	with open('03_Notebooks/03_System/app_risks/pipe_execution_pd.pickle', mode='rb') as file:
		pipe_execution_pd = pickle.load(file)

	with open('03_Notebooks/03_System/app_risks/pipe_execution_ead.pickle', mode='rb') as file:
		pipe_execution_ead = pickle.load(file)

	with open('03_Notebooks/03_System/app_risks/pipe_execution_lgd.pickle', mode='rb') as file:
		pipe_execution_lgd = pickle.load(file)


	#6.EXECUTION
	scoring_pd = pipe_execution_pd.predict_proba(x_pd)[:, 1]
	ead = pipe_execution_ead.predict(x_ead)
	lgd = pipe_execution_lgd.predict(x_lgd)


	#7.RESULT
	principal = x_pd.principal
	EL = pd.DataFrame({'principal':principal,
		               'pd':scoring_pd,
		               'ead':ead,
		               'lgd':lgd                   
		               })
	EL['expected_loss'] = round(EL.pd * EL.principal * EL.ead * EL.lgd,2)

	return(EL)
