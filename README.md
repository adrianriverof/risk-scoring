
# Loan Risk Scoring with Machine Learning


## Overview

This project involves creating a model to calculate **expected loss in a banking risk context**. Using a loan dataset, different models are trained to estimate the **capital at risk** for that specific loan.

In addition, it includes a **Streamlit web application** that allows users to calculate loan risk using the trained models.

<br>
<p align="center">
	<a href="https://risk-score-analyzer-prototype.streamlit.app/">
		<img src="https://github.com/user-attachments/assets/26ebc28d-a412-4523-b3f9-23ff9ee94039" alt="" height="300"/>
	</a>
</p>
<!--
<img width="779" height="467" align="center" alt="app" src="https://github.com/user-attachments/assets/c2f369aa-4309-4231-b8b9-4aeab916bdd1" />
-->
<!--
<img width="520" height="311" alt="imagen" src="https://github.com/user-attachments/assets/00a2953d-8a7b-4853-992d-9b3dc5c5ee04" />
1558, 933
-->
<br>

## Risk Scoring Approach

The model follows the standard banking risk framework:

$$
EL = PD \times P \times EAD \times LGD
$$

Where:
- **EL** = Expected Loss (€)
- **PD** = Probability of Default (%)
- **P** = Principal (€)
- **LGD** = Loss Given Default (%)
- **EAD** = Exposure at Default (%)

In order to calculate the expected loss, the models would predict from the personal data:

- PD with a **Logistic Regression**
- LGD and EAD with **LightGBM**

*Typical elements of banking risk modeling (WOE, KS, information value, ...) were not used in order to keep this project more applicable to a general case*


## Process

1. Data preparation
	- Clean the data, group atypicals
	- Create new variables to get the target information for the estimation

2. Modeling
	- Optimize hyperparameters for the three models 
	- Prepare the final pipelines for production
	
3. Production
	- Scripts for retraining and execution of the predictive models
	- Build the [streamlit app](https://risk-score-analyzer-prototype.streamlit.app/) based on the predictive models


## Notebooks & Scripts

- [Development notebooks](https://github.com/adrianriverof/risk-scoring/tree/master/03_Notebooks/02_Development)  
- [Retraining script](https://github.com/adrianriverof/risk-scoring/blob/master/03_Notebooks/03_System/09_Retraining_code.py)
- [Execution script](https://github.com/adrianriverof/risk-scoring/blob/master/03_Notebooks/03_System/10_Execution_code.py)
- [Streamlit app code](https://github.com/adrianriverof/risk-scoring/blob/master/03_Notebooks/03_System/app_risks/app_risks.py)


## Installation

Clone the repository and install dependencies:

```bash
conda env create -f 01_Documents/risks.yml
conda activate risks
```



