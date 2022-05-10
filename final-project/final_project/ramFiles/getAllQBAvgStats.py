import pandas as pd
import csv

df = pd.read_csv('data/qbStats.csv', dtype={
                    'QB Name': 'str',
                    'Year': 'int64',
                    'Completed Passes': 'float64',
                    'Attempted Passes': 'float64',
                   # 'Catch Percentage': 'float64',
                    'Passing Touchdowns': 'float64',
                    'Interceptions Thrown': 'float64',
                    'Passing Yards per Attempt': 'float64',
                    'Interception Percentage': 'float64',
                    'Quarterback Rating': 'float64',
                    'Yards Per Game Played': 'float64',
                    'Passing Yards per Attempt': 'float64',
                   # 'Fourth Quarter Comebacks': 'float64',
                    'Passing Yards': 'float64',
                 })

averages = {}
for index, row in df.iterrows():
   if row['QB Name'] in averages:
      years = averages[row['QB Name']]["years"] + 1
      completed_passes = (averages[row['QB Name']]["Completed Passes"] + row["Completed Passes"])*1.0/years
      attempted_passes = (averages[row['QB Name']]["Attempted Passes"] + row["Attempted Passes"])*1.0/years
    #  catch_percentage = (averages[row['QB Name']]["Catch Percentage"] + row["Catch Percentage"])*1.0/years
      passing_touchdowns = (averages[row['QB Name']]["Passing Touchdowns"] + row["Passing Touchdowns"])*1.0/years
      interceptions_thrown = (averages[row['QB Name']]["Interceptions Thrown"] + row["Interceptions Thrown"])*1.0/years
      passing_yards_per_attempt = (averages[row['QB Name']]["Passing Yards per Attempt"] + row["Passing Yards per Attempt"])*1.0/years
      interception_percentage = (averages[row['QB Name']]["Interception Percentage"] + row["Interception Percentage"])*1.0/years
      quarterback_rating = (averages[row['QB Name']]["Quarterback Rating"] + row["Quarterback Rating"])*1.0/years
      yards_per_game_played = (averages[row['QB Name']]["Yards Per Game Played"] + row["Yards Per Game Played"])*1.0/years
     # fourth_quarter_comebacks = (averages[row['QB Name']]["Fourth Quarter Comebacks"] + row["Fourth Quarter Comebacks"])*1.0/years
      passing_yards = (averages[row['QB Name']]["Passing Yards"] + row["Passing Yards"])*1.0/years

      averages.update({row['QB Name']:{
                     "years" : years,
                     "Completed Passes" : completed_passes,
                     "Attempted Passes" : attempted_passes,
                   #  "Catch Percentage" : catch_percentage,
                     "Passing Touchdowns" : passing_touchdowns,
                     "Interceptions Thrown" : interceptions_thrown,
                     "Passing Yards per Attempt" : passing_yards_per_attempt,
                     "Interception Percentage" : interception_percentage,
                     "Quarterback Rating" : quarterback_rating,
                     "Yards Per Game Played" : yards_per_game_played,
                  #   "Fourth Quarter Comebacks" : fourth_quarter_comebacks,
                     "Passing Yards" : passing_yards
      }})
   else:
       averages.update({row['QB Name']:{
                     "years" : 1,
                     "Completed Passes" : row["Completed Passes"],
                     "Attempted Passes" : row["Attempted Passes"],
                 #    "Catch Percentage" : row["Catch Percentage"],
                     "Passing Touchdowns" : row["Passing Touchdowns"],
                     "Interceptions Thrown" : row["Interceptions Thrown"],
                     "Passing Yards per Attempt" : row["Passing Yards per Attempt"],
                     "Interception Percentage" : row["Interception Percentage"],
                     "Quarterback Rating" : row["Quarterback Rating"],
                     "Yards Per Game Played" : row["Yards Per Game Played"],
                #     "Fourth Quarter Comebacks" : row["Fourth Quarter Comebacks"],
                     "Passing Yards" : row["Passing Yards"]
      }})

avgCSV = []
for key, value in averages.items():
   newRow = [key]
   for k, v in value.items():
      newRow.append(v)
   avgCSV.append(newRow)

f = open('data/avgStats.csv', 'w')

writer = csv.writer(f)
writer.writerow(["QB Name","Years", "Completed Passes","Attempted Passes","Passing Touchdowns","Interceptions Thrown","Passing Yards per Attempt","Interception Percentage","Quarterback Rating","Yards Per Game Played","Passing Yards"])

for avg in avgCSV:
    writer.writerow(avg)
