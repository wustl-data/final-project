# Run this app with `python dashboards/app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
# open a new terminal window (Ctrl+Shift+` in VS Code.)

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import plotly.io as pio
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import lrmodel
from lrmodel import prepareModel
import getQBAvgStats
from getQBAvgStats import getSelectedQbStats
from sportsreference.nfl.teams import Teams

app = Dash(external_stylesheets=[dbc.themes.VAPOR])

years_options = ['2021', '2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2006',
'2005','2004','2003','2002','2001','2000']
teams = Teams()
team_abbr = {}
for team in teams:
    team_abbr[team.name] = team.abbreviation
print(team_abbr)

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





if __name__ == "__main__":
    app.run_server(debug=True)
