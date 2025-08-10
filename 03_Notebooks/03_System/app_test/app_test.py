

import pandas as pd
import seaborn as sns
import streamlit as st

df = sns.load_dataset('tips')

seleccion = st.selectbox('Choose:',['Male','Female'])

df.loc[df.sex == seleccion]



