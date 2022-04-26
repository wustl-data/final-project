from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import data_cleaning as dc
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = dc.get_completed_passes_df()

color = ['green','yellow','orange','red']
down = ['First', 'Second', 'Third', 'Fourth']
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label = 'Weighting Contextually Important Completions', children =[
            dcc.Graph(id='scatter_plot'),
            dcc.Checklist(df['down'].unique(), id="check")
        ])
    ])
    
])
@app.callback(Output('scatter_plot', "figure"), Input('check', 'options'))
def update_scatter(input):
    df['down'] = df['down'].astype(str)
    return px.scatter(df, x='playResult', y='epaYards', color ='down', symbol ='down')


if __name__ == '__main__':
    app.run_server(debug=True)
 