import sportsipy
from sportsipy.nfl.roster import Player
from sportsipy.nfl.teams import Teams

print("hello")

brees = Player('BreeDr00')
print(brees.name)  # Prints 'Drew Brees'
print(brees.passing_yards)  # Prints Brees' career passing yards
# Prints a Pandas DataFrame of all relevant stats per season for Brees
print(brees.dataframe)
