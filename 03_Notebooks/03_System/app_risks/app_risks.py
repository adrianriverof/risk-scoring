
from execution_code import *
import streamlit as st
from streamlit_echarts import st_echarts

#PAGE CONFIGURATION
st.set_page_config(
     page_title = 'Risk Score Analyzer',
     layout = 'wide')

#SIDEBAR
with st.sidebar:
    #st.image('risk_score.jpg')

    #INPUTS
    principal = st.number_input('Requested Quantity', 500, 50000)
    purpose = st.selectbox('Purpose of the loan', ['debt_consolidation','credit_card','home_improvement','other'])
    num_installments = st.radio('Number of installments', ['36 months','60 months'])
    income = st.slider('Annual income', 20000, 300000)

    #KNOWN DATA (as static data for simplicity)
    verified_income = 'Verified'
    employment_duration = '10+ years'
    rating = 'B'
    dti = 28
    num_credit_lines = 3
    pct_revolving_utilization = 50
    interest_rate = 7.26
    installment_amount = 500
    num_derogatories = 0
    housing = 'MORTGAGE'




#MAIN
st.title('Risk Score Analyzer')


#CALCULATE

# Create the entry
entry = pd.DataFrame({'verified_income':verified_income,
                         'housing':housing,
                         'purpose':purpose,
                         'num_installments':num_installments,
                         'employment_duration':employment_duration,
                         'rating':rating,
                         'income':income,
                         'dti':dti,
                         'num_credit_lines':num_credit_lines,
                         'pct_revolving_utilization':pct_revolving_utilization,
                         'principal':principal,
                         'interest_rate':interest_rate,
                         'installment_amount':installment_amount,
                         'num_derogatories':num_derogatories}
                        ,index=[0])



#CALCULATE RISK
if st.sidebar.button('CALCULATE RISK'):
    #Execute scoring
    EL = execute_models(entry)

    #Calculate kpis
    kpi_pd = int(EL.pd * 100)
    kpi_ead = int(EL.ead * 100)
    kpi_lgd = int(EL.lgd * 100)
    kpi_el = int(EL.principal * EL.pd * EL.ead * EL.lgd)

    #Velocimeters
    # https://towardsdatascience.com/5-streamlit-components-to-build-better-applications-71e0195c82d4
    pd_options = {
            "tooltip": {"formatter": "{a} <br/>{b} : {c}%"},
            "series": [
                {
                    "name": "PD",
                    "type": "gauge",
                    "axisLine": {
                        "lineStyle": {
                            "width": 10,
                        },
                    },
                    "progress": {"show": "true", "width": 10},
                    "detail": {"valueAnimation": "true", "formatter": "{value}"},
                    "data": [{"value": kpi_pd, "name": "PD"}],
                }
            ],
        }

    #Velocimeter for ead
    ead_options = {
            "tooltip": {"formatter": "{a} <br/>{b} : {c}%"},
            "series": [
                {
                    "name": "EAD",
                    "type": "gauge",
                    "axisLine": {
                        "lineStyle": {
                            "width": 10,
                        },
                    },
                    "progress": {"show": "true", "width": 10},
                    "detail": {"valueAnimation": "true", "formatter": "{value}"},
                    "data": [{"value": kpi_ead, "name": "EAD"}],
                }
            ],
        }

    #Velocimeter for lgd
    lgd_options = {
            "tooltip": {"formatter": "{a} <br/>{b} : {c}%"},
            "series": [
                {
                    "name": "LGD",
                    "type": "gauge",
                    "axisLine": {
                        "lineStyle": {
                            "width": 10,
                        },
                    },
                    "progress": {"show": "true", "width": 10,},
                    "detail": {"valueAnimation": "true", "formatter": "{value}"},
                    "data": [{"value": kpi_lgd, "name": "LGD"}],
                }
            ],
        }
    # Represent them in app
    col1,col2,col3 = st.columns(3)
    with col1:
        st_echarts(options=pd_options, width="110%", key='0')
    with col2:
        st_echarts(options=ead_options, width="110%", key='1')
    with col3:
        st_echarts(options=lgd_options, width="110%", key='2')

    #Prescripcion
    col1,col2 = st.columns(2)
    with col1:
        st.write('The expected loss is (Euros):')
        st.metric(label="Expected Loss", value = kpi_el)
    with col2:
        st.write('Recommended additional interest rate (Euros):')
        st.metric(label="Fee to Apply", value = kpi_el * 3) #static for simplicity
else:
    st.write('Define the parameters of the loan and click on "Calculate Risk"')
    
    
    
    
