# Run this app with `python dashboards/app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
# open a new terminal window (Ctrl+Shift+` in VS Code.)
from cProfile import label
from turtle import title
import dash
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import plotly.io as pio
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np


from sportsreference.nfl.teams import Teams
import ramFiles.lrmodel
from ramFiles.lrmodel import prepareModel
import ramFiles.getQBAvgStats
from ramFiles.getQBAvgStats import getSelectedQbStats

## Hannah's setup
from sportsreference.nfl.roster import Player
from sportsreference.nfl.teams import Teams
from sportsreference.nfl.schedule import Schedule
import hannahFiles.college
from hannahFiles.college import get_rush_attempts, get_rush_attempts_per_game, get_rush_td, get_rush_yards, get_rush_yards_per_attempt, get_times_pass_target, get_yards_per_touch
import matplotlib.pyplot as plt

# players to look at from Wisconsin
jonathon_taylor = "TaylJo02"
james_white = "WhitJa02"
melvin_gordon = "GordMe00"
dare_ogum = "OgunDa00"
corey_clement = "ClemCo00"

jt = Player(jonathon_taylor)
jw = Player(james_white)
mg = Player(melvin_gordon)
do = Player(dare_ogum)
cc = Player(corey_clement)
wisc = [jt, jw, mg, do, cc]
name = ["Jonathon Taylor", "James White", "Melvin Gordon", "Dare Ogumbowale", "Corey Clement"]
## end Hannah setup

app = Dash(external_stylesheets=[dbc.themes.VAPOR])

#Gus's setup
years_options = ['2021', '2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2006',
'2005','2004','2003','2002','2001','2000']
teams = Teams()
team_abbr = {}
team_names = []
for team in teams:
    team_abbr[team.name] = team.abbreviation
    team_names.append(team.name)
#End Gus's setup

#Start Matt's Setup
from mattFiles.data_cleaning import get_completed_passes_df
from mattFiles.data_cleaning import get_incompleted_passes_df
from mattFiles.data_cleaning import completion_teams_description
from mattFiles.data_cleaning import incompletion_teams_description
completed_passes_df = get_completed_passes_df()
incompleted_passes_df = get_incompleted_passes_df()
comp_desc = completion_teams_description()
incomp_desc = incompletion_teams_description()
#End Matts's Setup

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='QB Economic Model (Fill in Stats)', children=[
            dcc.Input(id="years", type="text", placeholder="Years Played", style={'marginRight':'10px'}),
            dcc.Input(id="completedPasses", type="text", placeholder="Completed Passes", style={'marginRight':'10px'}),
            dcc.Input(id="attemptedPasses", type="text", placeholder="Attempted Passes", style={'marginRight':'10px'}),
            dcc.Input(id="passingTds", type="text", placeholder="Passing Touchdowns", style={'marginRight':'10px'}),
            dcc.Input(id="ints", type="text", placeholder="Interceptions", style={'marginRight':'10px'}),
            dcc.Input(id="ydpergame", type="text", placeholder="Yards per game played", style={'marginRight':'10px'}),
            dcc.Input(id="passingYards", type="text", placeholder="Passing Yards", style={'marginRight':'10px'}),
            html.Div(id="output")
        ]),
        dcc.Tab(label='QB Economic Model (Choose from Players)', children=[
            dcc.Dropdown(['Tom Brady', 'Aaron Rodgers', 'Patrick Mahomes', 'Josh Allen','Matthew Stafford','Dak Prescott','Derek Carr','Ryan Tannehill','Kirk Cousins','Matt Ryan','Jimmy Garoppolo','Teddy Bridgewater','Carson Wentz','Jameis Winston','Jared Goff','Deshaun Watson','Mitchell Trubisky','Taylor Heinicke'], 'Tom Brady', id='qb-dropdown'),
            html.Div(id="output2")
        ]),
        dcc.Tab(label='College Effect', children=[
            dcc.Dropdown(['Career Rush Attempts', 'Career Rush Attempts per Game', 'Career Rushing Touchdowns', 'Career Rushing Yards', 'Career Rush Yards per Attempt', 'Career Times Pass Target', 'Career Yards per Touch'], 'Career Yards per Touch', id='college-dropdown'),
            html.Div(id="college-graphs")
        ]),
        dcc.Tab(label='Fourth Down Rate', children=[
            dcc.Dropdown(team_names, 'Chicago Bears', id = 'team-name-dropdown'),
            dcc.Dropdown(years_options, '2021', id = 'year-option-dropdown'),
            html.Div(id = 'fourth-down-graph'),
        ]),
        dcc.Tab(label='Third Down Rate', children=[
            dcc.Dropdown(team_names, 'Chicago Bears', id = 'third-team-name-dropdown'),
            dcc.Dropdown(years_options, '2021', id = 'third-year-option-dropdown'),
            html.Div(id = 'third-down-graph'),
        ]),
        dcc.Tab(label='Game Impact', children =[
            dcc.Graph(id='completions_full'),
            dcc.Checklist(completed_passes_df['down'].unique,['1'], id = 'completions_full_check'),
            dcc.Graph(id ='incompletions_full'),
            dcc.Checklist(completed_passes_df['down'].unique,['1'], id = 'incompletions_full_check'),
        ])
    ])
])

#Gus's callback for fourth down conversion rate
@app.callback([Output('fourth-down-graph', 'children')],
              [Input('team-name-dropdown', 'value'),
              Input('year-option-dropdown', 'value')])
def fourth_choose_team_and_year(team,year):
    """changes graph based on team and year selected from dropdowns, initialized with the Chicago Bear's 2021 season

    Args:
        team (list of str): Selected team from dropdown
        year (list of str): Selected year from dropdown

    Returns:
        figure: Scatterplot of fourth down conversion rate for the team and year selected, na values omitted from plot
    """
    schedule = Schedule(team_abbr[team], year)
    fourth_down_rate = []
    fourth_down_conv = schedule.dataframe.fourth_down_conversions
    fourth_down_att = schedule.dataframe.fourth_down_attempts
    fourth_down_rate = (fourth_down_conv/fourth_down_att)
    fourth_down_rate_cleaned = fourth_down_rate.dropna()
  
    fig = px.scatter(x = fourth_down_rate_cleaned.index, y = fourth_down_rate_cleaned.values, color = fourth_down_rate_cleaned.values > 0.5, 
    title = u'Fourth Down Conversion Rate Scatterplot for the {}'.format(team), labels = {'x': 'GameCodes', 'y': 'Conversion Rate'})
    return [html.Div([
        dcc.Graph(figure = fig, id = 'fourth-graph')
    ])]

#Gus's callback for third down conversion rate
@app.callback([Output('third-down-graph', 'children')],
              [Input('third-team-name-dropdown', 'value'),
              Input('third-year-option-dropdown', 'value')])
def third_choose_team_and_year(team,year):
    """changes graph based on team and year selected from dropdowns, initialized with the Chicago Bear's 2021 season

    Args:
        team (list of str): Selected team from dropdown
        year (list of str): Selected year from dropdown

    Returns:
        figure: Scatterplot of third down conversion rate for the team and year selected, na values omitted from plot
    """
    schedule = Schedule(team_abbr[team], year)
    third_down_rate = []
    third_down_conv = schedule.dataframe.third_down_conversions
    third_down_att = schedule.dataframe.third_down_attempts
    third_down_rate = (third_down_conv/third_down_att)
    third_down_rate_cleaned = third_down_rate.dropna()
  
    fig = px.scatter(x = third_down_rate_cleaned.index, y = third_down_rate_cleaned.values, color = third_down_rate_cleaned.values > 0.35, 
    title = u'Third Down Conversion Rate Scatterplot for the {}'.format(team), labels = {'x': 'GameCodes', 'y': 'Conversion Rate'})
    return [html.Div([
        dcc.Graph(figure = fig, id = 'third-graph')
    ])]

@app.callback(
    Output("output", "children"),
    Input("years", "value"),
    Input("completedPasses", "value"),
    Input("attemptedPasses", "value"),
    Input("passingTds", "value"),
    Input("ints", "value"),
    Input("ydpergame", "value"),
    Input("passingYards", "value"),
)
def update_output(years, completedPasses, attemptedPasses, passingTds,ints,ydpergame,passingYards):
    if(years is None or completedPasses is None or attemptedPasses is None or passingTds is None or ints is None or ydpergame is None or passingYards is None):
        return "Please fill in first"
    model = prepareModel()
    newX = [[years,completedPasses,attemptedPasses,passingTds,ints,ydpergame,passingYards]]
    y_pred = model.predict(newX)
    return u'Expected Salary: ${}'.format(y_pred)


@app.callback(
    Output("output2", "children"),
    Input("qb-dropdown", "value"),
)
def update_output2(value):
    newX = getSelectedQbStats(value)
    model = prepareModel()
    y_pred = model.predict([newX])
    return u'Expected Salary: ${}'.format(y_pred)

@app.callback(Output('college-graphs', 'children'),
              Input('college-dropdown', 'value'))
def render_content(graph):
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    if graph == 'Career Rush Attempts':
        fig = px.bar(x = name, y = get_rush_attempts(wisc), color = name, hover_name = name)
        return html.Div([
            dcc.Graph(figure = fig, id='rush-attempts-graph'),
            html.Hr()
        ])
    elif graph == 'Career Rush Attempts per Game':
        fig = px.bar(x = name, y = get_rush_attempts_per_game(wisc), color = name, hover_name = name)
        return html.Div([
            dcc.Graph(figure = fig, id='rush-att-gm-graph'),
            html.Hr()
        ])
    elif graph == 'Career Rushing Touchdowns':
        fig = px.bar(x = name, y = get_rush_td(wisc), color = name, hover_name = name)
        return html.Div([
            dcc.Graph(figure = fig, id='rushtd-graph'),
            html.Hr()
        ])
    elif graph == 'Career Rushing Yards':
        fig = px.bar(x = name, y = get_rush_yards(wisc), color = name, hover_name = name)
        return html.Div([
            dcc.Graph(figure = fig, id='rush-yards-graph'),
            html.Hr()
        ])
    elif graph == 'Career Rush Yards per Attempt':
        fig = px.bar(x = name, y = get_rush_yards_per_attempt(wisc), color = name, hover_name = name)
        return html.Div([
            dcc.Graph(figure = fig, id='rush-yards-att-graph'),
            html.Hr()
        ])
    elif graph == 'Career Times Pass Target':
        fig = px.bar(x = name, y = get_times_pass_target(wisc), color = name, hover_name = name)
        return html.Div([
            dcc.Graph(figure = fig, id='pass-target-graph'),
            html.Hr(),
            "James White was targeted for passes significantly more, and likely took more of a wide receiver role which explains why his rushing stats are lower than the others despite having a longer career."
        ])
    elif graph ==  'Career Yards per Touch':
        fig = px.bar(x = name, y = get_yards_per_touch(wisc), color = name, hover_name = name)
        fig.add_hline(y = 4, annotation_text = "Average RB")
        fig.add_hline(y= 5, annotation_text = "Good RB")
        return html.Div([
            dcc.Graph(figure = fig, id='yards-touch-graph'),
            html.Hr(),
            "All Wisconsin RB have an average yards per touch for their career above the line for an average RB and several are above the limit for a good RB."
        ])

#Start of Matt's GameImpact Tab

#End of Matt's GameImpact Tab

if __name__ == "__main__":
    app.run_server(debug=True)
