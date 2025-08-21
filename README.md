
# Risk Scoring


## Overview





## Process

1. Data preparation
	- Clean the data, group atypicals
	- Create new variables to get the target information for the estimation

2. Modeling
	- Optimize hyperparameters for the three models 
	- Prepare the final pipelines for production
	
3. Production
	- Scripts for retraining and execution of the predictive models
	- Build the [streamlit app](https://risk-score-analyzer-prototype.streamlit.app/) based on the predictive systems


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

