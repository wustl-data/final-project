from sportsreference.nfl.schedule import Schedule
from sportsreference.nfl.boxscore import Boxscore
mil2019 = Schedule('ATL', year = '2019')
print(mil2019.dataframe.columns)

at2019 = Boxscore('201909080min')
print(at2019.dataframe.columns)