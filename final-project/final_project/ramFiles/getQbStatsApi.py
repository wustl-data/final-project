import sportsipy
from sportsipy.nfl.roster import Player
from sportsipy.nfl.teams import Teams
from sportsipy.nfl.roster import Roster
import pandas as pd
import csv

    """This file reads in the dates from the last contract for the QBs and then uses the Sports Reference API to get the QB's statistics from these years. 
       This data is stored in a file called qbStats.csv.
    """

dataset = pd.read_csv("data/salaryData.csv", header=None)
skippedFirst = False
stats = []
for row_index, row in dataset.iterrows():

    if(skippedFirst):
        names = row[0].split(" ")
        firstName = names[0]
        lastName = names[1]
    
        number = "00"
        if(row[0] == "Derek Carr" or row[0] == "Josh Allen"):
            number = "02"
        if(row[0] == "Dak Prescott"):
            number = "01"
            
        apiId = lastName[0:4] + firstName[0:2] + number
        
        player = Player(apiId)
        dates = row[5].split("-")
        currentYear = int(dates[0])
        while(currentYear <= int(dates[1])):
            
            completed_passes = player(str(currentYear)).completed_passes
            attempted_passes = player(str(currentYear)).attempted_passes 
            passing_touchdowns = player(str(currentYear)).passing_touchdowns
            interceptions_thrown = player(str(currentYear)).interceptions_thrown
            passing_yards_per_attempt = player(str(currentYear)).passing_yards_per_attempt
            interception_percentage = player(str(currentYear)).interception_percentage
            quarterback_rating = player(str(currentYear)).quarterback_rating
            yards_per_game_played = player(str(currentYear)).yards_per_game_played
            passing_yards_per_attempt = player(str(currentYear)).passing_yards_per_attempt
            passing_yards = player(str(currentYear)).passing_yards

            newRow = [row[0],currentYear,completed_passes,attempted_passes,passing_touchdowns,interceptions_thrown,passing_yards_per_attempt,interception_percentage,quarterback_rating,yards_per_game_played,passing_yards_per_attempt,passing_yards]
            print(newRow)
            stats.append(newRow)
            if(None in newRow):
                print(newRow)
            currentYear += 1
    skippedFirst = True

f = open('data/qbStats.csv', 'w')

writer = csv.writer(f)
writer.writerow(["QB Name","Year", "Completed Passes","Attempted Passes","Passing Touchdowns","Interceptions Thrown","Passing Yards per Attempt","Interception Percentage","Quarterback Rating","Yards Per Game Played","Passing Yards per Attempt","Passing Yards"])

for stat in stats:
    writer.writerow(stat)
