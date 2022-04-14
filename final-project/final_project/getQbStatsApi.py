import sportsipy
from sportsipy.nfl.roster import Player
from sportsipy.nfl.teams import Teams
from sportsipy.nfl.roster import Roster
import pandas as pd
import csv

dataset = pd.read_csv("data/salaryData.csv", header=None)
skippedFirst = False
stats = []
for row_index, row in dataset.iterrows():
   # print(row[0])
   # print(row[5])
    if(skippedFirst):
        names = row[0].split(" ")
        firstName = names[0]
        lastName = names[1]

        number = "00"
        if(row[0] == "Derek Carr" or row[0] == "Josh Allen"):
            number = "02"
        apiId = lastName[0:4] + firstName[0:2] + number
     #   print(apiId)
        player = Player(apiId)
       # print(player.name)  # Prints 'Drew Brees'
      #  print(player.passing_yards)  # Prints Brees' career passing yards
        # Prints a Pandas DataFrame of all relevant stats per season for Brees
        #print(player.dataframe)
        dates = row[5].split("-")
        currentYear = int(dates[0])
        while(currentYear <= int(dates[1])):
            completed_passes = player(str(currentYear)).completed_passes
            attempted_passes = player(str(currentYear)).attempted_passes 
            catch_percentage = player(str(currentYear)).catch_percentage
            passing_touchdowns = player(str(currentYear)).passing_touchdowns
            interceptions_thrown = player(str(currentYear)).interceptions_thrown
            passing_yards_per_attempt = player(str(currentYear)).passing_yards_per_attempt
            interception_percentage = player(str(currentYear)).interception_percentage
            quarterback_rating = player(str(currentYear)).quarterback_rating
            yards_per_game_played = player(str(currentYear)).yards_per_game_played
            passing_yards_per_attempt = player(str(currentYear)).passing_yards_per_attempt
            fourth_quarter_comebacks = player(str(currentYear)).fourth_quarter_comebacks
            passing_yards = player(str(currentYear)).passing_yards

            stats.append([row[0],currentYear,completed_passes,attempted_passes,catch_percentage,passing_touchdowns,interceptions_thrown,passing_yards_per_attempt,interception_percentage,quarterback_rating,yards_per_game_played,passing_yards_per_attempt,fourth_quarter_comebacks,passing_yards])
            currentYear += 1
    skippedFirst = True

f = open('data/qbStats.csv', 'w')

writer = csv.writer(f)
writer.writerow(["QB Name","Year", "Completed Passes","Attempted Passes","Catch Percentage","Passing Touchdowns","Interceptions Thrown","Passing Yards per Attempt","Interception Percentage","Quarterback Rating","Yards Per Game Played","Passing Yards per Attempt","Fourth Quarter Comebacks","Passing Yards"])

for stat in stats:
    writer.writerow(stat)


    # stats needed - cmp, att, cmp%, yds, td, int, int%, 1D, rate, y/a, gwd, awards


