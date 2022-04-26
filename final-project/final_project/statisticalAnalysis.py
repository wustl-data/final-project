import pandas as pd
import numpy as np

    """This file is simply for doing some statistical analysis on the datasets I prepared.
    """

salary_df = pd.read_csv('data/salaryData.csv', dtype={
                    'QB Name': 'str',
                    'Number of Years on Contract': 'float64',
                    'Total Contract Size': 'float64',
                    'Salary per Year': 'float64',
                    'Age': 'float64',
                    'Previous Contract Years': 'str'
                })
    
salaries = []

def q1(x):
    return x.quantile(0.1)

def q2(x):
    return x.quantile(0.5)

def q3(x):
    return x.quantile(0.9)

salary_df = salary_df[["Salary per Year"]]
vals = {'Salary per Year': [q1, q2, q3]}    

print(salary_df.describe())
print(salary_df)