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
            dcc.Dropdown(['Career Yards', 'Career Yards/Touch', 'Combined'], 'Combined', id='college-dropdown'),
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
    name = [jt.name, jw.name, mg.name, do.name, cc.name]
    yards = [jt.rush_yards, jw.rush_yards, mg.rush_yards, do.rush_yards, cc.rush_yards]
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    ypt = [(jt.rush_yards/jt.touches), (jw.rush_yards/jw.touches), (mg.rush_yards/mg.touches), (do.rush_yards/do.touches), (cc.rush_yards/cc.touches)]

    if graph == 'Combined':
        fig = px.scatter(x = yards, y = ypt, color = name, hover_name = name)
        return html.Div([
            dcc.Graph(figure = fig, id='combinedgraph'),
            html.Hr()
        ])
    elif graph == 'Career Yards/Touch':
        fig = px.bar(x = name, y = ypt, color = name, hover_name = name)
        return html.Div([
            dcc.Graph(figure = fig, id='cyptgraph'),
            html.Hr()
        ])
    elif graph == 'Career Yards':
        fig = px.bar(x = name, y = yards, color = name, hover_name = name)
        return html.Div([
            dcc.Graph(figure = fig, id='cyardsgraph'),
            html.Hr()
        ])

if __name__ == "__main__":
    app.run_server(debug=True)
