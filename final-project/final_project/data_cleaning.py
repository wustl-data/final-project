from pathlib import Path
import pandas as pd

def get_completed_passes_df():
    path = Path(__file__).parent / "../data/nfl-big-data-bowl-2021/plays.csv"
    plays_df = pd.read_csv(path)
    completions_df = plays_df.loc[plays_df['passResult'] == 'C']
    positive_yards_df = completions_df.loc[completions_df['playResult'] > 0]
    filter_df = positive_yards_df.loc[positive_yards_df['playDescription'].str.contains('FUMBLE') == False]
    filter_df['epaYards'] = filter_df.loc[:,'playResult']
    filter_df.loc[filter_df['playResult']>= filter_df['yardsToGo'],'epaYards'] = filter_df['epaYards']*(0.75+ filter_df['down']/4)
    filter_df.loc[filter_df['playDescription'].str.contains('TOUCHDOWN')] = filter_df['epaYards']*1.6
    return filter_df
get_completed_passes_df()

