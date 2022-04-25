import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
import csv

def prepareModel():
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

   x = []

   for index, row in stats_df.iterrows():
      newRow = []

      newRow.append(row["Years"])
      newRow.append(row["Completed Passes"])
      newRow.append(row["Attempted Passes"])
   
      #newRow.append(row["Catch Percentage"])
      newRow.append(row["Passing Touchdowns"])
      newRow.append(row["Interceptions Thrown"])
      
      # newRow.append(row["Passing Yards per Attempt"])
      # newRow.append(row["Interception Percentage"])
   #  newRow.append(row["Quarterback Rating"])
      newRow.append(row["Yards Per Game Played"])
      # newRow.append(row["Fourth Quarter Comebacks"])
   
      newRow.append(row["Passing Yards"])

      x.append(newRow)


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
      y.append(row["Salary per Year"])

   x, y = np.array(x), np.array(y)

   model = LinearRegression().fit(x, y)
   return model
""" 
r_sq = model.score(x, y)
print('coefficient of determination:', r_sq)
#print('intercept:', model.intercept_)
#print('slope:', model.coef_)
years = float(input("Enter years: "))
completed_passes = float(input("Completed Passes: "))
attempted_passes = float(input("Attempted Passes: "))

passing_touchdowns = float(input("Passing Touchdowns: "))
interceptions_thrown = float(input("Interceptions Thrown: "))

#pass_yd_per_attempt = float(input("Passing yds per attempt: "))
#interception_per = float(input("Interception percentage: "))
#qb_rating = float(input("QB Rating: "))
yd_per_game = float(input("Yards per game played: "))

passing_yds = float(input("Passing Yards: "))

#newX = [[years,completed_passes,attempted_passes, passing_touchdowns,interceptions_thrown, pass_yd_per_attempt,interception_per,qb_rating,yd_per_game,passing_yds]]
#newX = [[years,completed_passes,attempted_passes,passing_yds,passing_touchdowns,interceptions_thrown,yd_per_game]]
y_pred = model.predict(x)
print('predicted response:', y_pred, sep='\n')
   """