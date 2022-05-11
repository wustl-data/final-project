from pathlib import Path
import pandas as pd
pd.options.mode.chained_assignment = None

def get_completed_passes_df():
    path = Path(__file__).parent / "data/nfl-big-data-bowl-2021/plays.csv"
    plays_df = pd.read_csv(path)
    completions_df = plays_df.loc[plays_df['passResult'] == 'C']
    positive_yards_df = completions_df.loc[completions_df['playResult'] > 0]
    filter_df = positive_yards_df.loc[positive_yards_df['playDescription'].str.contains('FUMBLE') == False]
    filter_df['epaYards'] = filter_df.loc[:,'playResult']
    filter_df.loc[filter_df['playResult']>= filter_df['yardsToGo'],'epaYards'] = filter_df['epaYards']*(0.75+ filter_df['down']/4)
    filter_df.loc[filter_df['playDescription'].str.contains('TOUCHDOWN'), 'epaYards'] = filter_df['epaYards']*1.6
    filter_df.loc[abs(filter_df['preSnapVisitorScore']-filter_df['preSnapHomeScore'])<=10, 'epaYards'] = filter_df['epaYards']*(0.9+filter_df['quarter']/10)
    return filter_df

def get_incompleted_passes_df():
    path = Path(__file__).parent / "data/nfl-big-data-bowl-2021/plays.csv"
    plays_df = pd.read_csv(path)
    incompletions_df = plays_df.loc[plays_df['passResult']=='I']
    filter_df = incompletions_df.loc[incompletions_df['playDescription'].str.contains('sack') == False]
    filter_df = filter_df.loc[incompletions_df['playDescription'].str.contains('PENALTY') == False]
    filter_df = filter_df.loc[incompletions_df['playDescription'].str.contains('FUMBLE') == False]
    filter_df = filter_df.loc[incompletions_df['playDescription'].str.contains('Intentional Grounding') == False]
    filter_df = filter_df.loc[incompletions_df['playDescription'].str.contains('Roughness') == False]
    filter_df['epaYardsOp'] = filter_df['epa']+filter_df['epa']*(filter_df['down']-1)
    filter_df.loc[abs(filter_df['preSnapVisitorScore']-filter_df['preSnapHomeScore'])<=10, 'epaYardsOp'] = filter_df['epaYardsOp']*(0.9+filter_df['quarter']/10)
    filter_df.loc[filter_df['absoluteYardlineNumber']<=45,'epaYardsOp'] = filter_df['epaYardsOp']*(1+(45-filter_df['absoluteYardlineNumber'])/30)
    return filter_df

def completion_teams_description():
    full_df = get_completed_passes_df()
    select_df = pd.DataFrame().assign(possessionTeam = full_df['possessionTeam'], epaYards = full_df['epaYards'])
    df = select_df.groupby(['possessionTeam']).describe()
    df.columns = df.columns.droplevel(0)
    return df

def incompletion_teams_description():
    full_df = get_incompleted_passes_df()
    select_df = pd.DataFrame().assign(possessionTeam = full_df['possessionTeam'], epaYardsOp = full_df['epaYardsOp'])
    df = select_df.groupby(['possessionTeam']).describe()
    df.columns = df.columns.droplevel(0)
    return df
