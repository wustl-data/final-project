import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
import csv

def getSelectedQbStats(qbName):
    stats_df = pd.read_csv('data/avgStats.csv', dtype={
                     'QB Name': 'str',
                     'Years': 'int64',
                     'Completed Passes': 'float64',
                     'Attempted Passes': 'float64',
                     #'Catch Percentage': 'float64',
                     'Passing Touchdowns': 'float64',
                     'Interceptions Thrown': 'float64',
                     #'Passing Yards per Attempt': 'float64',
                     'Interception Percentage': 'float64',
                     #'Quarterback Rating': 'float64',
                     'Yards Per Game Played': 'float64',
                     # 'Fourth Quarter Comebacks': 'float64',
                     'Passing Yards': 'float64',
                  })
    
    rows = stats_df.loc[stats_df['QB Name'] == qbName]

    return [rows['Years'].values[0],rows['Completed Passes'].values[0], rows['Attempted Passes'].values[0],rows['Passing Touchdowns'].values[0],rows['Interceptions Thrown'].values[0], rows['Yards Per Game Played'].values[0],rows['Passing Yards'].values[0]]
   