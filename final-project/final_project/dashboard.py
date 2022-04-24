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

app = Dash(external_stylesheets=[dbc.themes.VAPOR])

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='QB Economic Model', children=[
            dcc.Input(id="years", type="text", placeholder="Years Played", style={'marginRight':'10px'}),
            dcc.Input(id="completedPasses", type="text", placeholder="Completed Passes", style={'marginRight':'10px'}),
            dcc.Input(id="attemptedPasses", type="text", placeholder="Attempted Passes", style={'marginRight':'10px'}),
            dcc.Input(id="passingTds", type="text", placeholder="Passing Touchdowns", style={'marginRight':'10px'}),
            dcc.Input(id="ints", type="text", placeholder="Interceptions", style={'marginRight':'10px'}),
            dcc.Input(id="ydpergame", type="text", placeholder="Yards per game played", style={'marginRight':'10px'}),
            dcc.Input(id="passingYards", type="text", placeholder="Passing Yards", style={'marginRight':'10px'}),
            html.Div(id="output")
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

if __name__ == "__main__":
    app.run_server(debug=True)
