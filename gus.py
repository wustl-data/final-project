from black import schedule_formatting
from sportsreference.nfl.schedule import Schedule
from sportsreference.nfl.roster import Player
from sportsreference.nfl.boxscore import Boxscore
from sportsreference.nfl.teams import Teams
import pandas as pd
import datetime


#Use schedule with team and year, iterate through all years, grabbing 4th down conversions and attempts for each team, then divide those numbers
#Outer loop would be year, inner loop would be going through each team
#Look at wins per team per year

date = datetime.datetime(2019,9,8)
sce = Schedule(date)
schedule = Schedule('ATL', year = '2019')

sce.dataframe.columns
sce.Boxscore_index
Schedule.dataframe.boxscore_index



# df = Boxscore('201908090min')
# print(df.away_points)
# print(df.summary)
# print(df.winner)


# df = pd.DataFrame()
# teamdf = Teams()
# print(teamdf)
# for team in teamdf:
#     schedule = team.schedule
#     df.append(team.schedule.dataframe_extended)
# home_fourth_conv = df.home_fourth_down_conversions
# home_fourth_att = df.home_fourth_down_attempts
# away_fourth_conv = df.away_fourth_down_conversions
# away_fourth_att = df.away_fourth_down_attempts
# home_fourth_down_rate = home_fourth_conv/ home_fourth_att
# away_fourth_down_rate = away_fourth_conv/ away_fourth_att
# print(home_fourth_down_rate, away_fourth_down_rate)

# home_conv = {}
# home_att = {}
# for team in Teams('2021'):
#     home_conv[team.name] = Boxscore(team.schedule.boxscore_index).home_fourth_down_conversions
#     home_att[team.name] = Boxscore.home_fourth_down_attempts



# teams = Teams()
# for team in teams.dataframes:
#     print(team.name)  # Prints the team's name
#     # Prints the team's average margin of victory
#     print(team.margin_of_victory)

# def print_most_wins(year, wins):
#     most_wins = max(wins, key=wins.get)
#     print('%s: %s - %s' % (year, wins[most_wins], most_wins))

# for year in range(2000, 2022):
#     wins = {}
#     for team in Teams(year):
#         wins[team.name] = team.wins
#     print_most_wins(year, wins)

# at2019 = Boxscore('201909080min')   