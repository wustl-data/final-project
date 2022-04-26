# Run this app with `python dashboards/app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
# open a new terminal window (Ctrl+Shift+` in VS Code.)

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import plotly.io as pio
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import ramFiles.lrmodel
from ramFiles.lrmodel import prepareModel
import ramFiles.getQBAvgStats
from ramFiles.getQBAvgStats import getSelectedQbStats

## Hannah's setup
from sportsreference.nfl.roster import Player
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
        ])
    ])
])

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
