import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv

    """This file creates scatter plots with best line of fit to see how strong the correlation is between different QB stats, like years and passing yards, and salary. 
       This was useful in figuring out which attributes are most important and should be used for the model with a visual representation
    """
# from these plots, I found out that Passing Yards per attempt, interception percentage, and qbr are all not that good. I also feel like some of this could be because of the "outliers" so I tried removing them and checked
# some of the plots, like interception percentage look a bit better, and some like qbr look very good, however for the time being, I will remove these three attributes
stats_df = pd.read_csv('data/avgStats.csv', dtype={
                    'QB Name': 'str',
                    'Years': 'int64',
                    'Completed Passes': 'float64',
                    'Attempted Passes': 'float64',
                    #'Catch Percentage': 'float64',
                    'Passing Touchdowns': 'float64',
                    'Interceptions Thrown': 'float64',
                    'Passing Yards per Attempt': 'float64',
                    'Interception Percentage': 'float64',
                    'Quarterback Rating': 'float64',
                    'Yards Per Game Played': 'float64',
                   # 'Fourth Quarter Comebacks': 'float64',
                    'Passing Yards': 'float64',
                 })

salary_df = pd.read_csv('data/salaryData.csv', dtype={
                    'QB Name': 'str',
                    'Number of Years on Contract': 'float64',
                    'Total Contract Size': 'float64',
                    'Salary per Year': 'float64',
                    'Age': 'float64',
                    'Previous Contract Years': 'str'
                 })
y = []

for index, row in salary_df.iterrows():
    if(row["QB Name"] == "Dak Prescott" or row["QB Name"] == "Mitchell Trubisky" or row["QB Name"] == "Taylor Heinicke"):
        continue
    y.append(row["Salary per Year"])

pY = np.array(y)

for column in stats_df:
    if column == "QB Name" or column == "Years":
        continue
    x = []

    for index, row in stats_df.iterrows():
        if(row["QB Name"] == "Dak Prescott" or row["QB Name"] == "Mitchell Trubisky" or row["QB Name"] == "Taylor Heinicke"):
            continue
        x.append(row[column])

    pX = np.array(x)

    plt.plot(pX, pY ,'o')
    m, b = np.polyfit(pX, pY, 1)
    plt.plot(pX, m*pX+b) 
    print(m)
    print(b)

    plt.xlabel(str(column))
    plt.ylabel('Salary ($)')
    plt.title(str(column))
    plt.show()
