from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from data_cleaning_Matt import get_completed_passes_df
from data_cleaning_Matt import get_incompleted_passes_df
from data_cleaning_Matt import completion_teams_description
from data_cleaning_Matt import incompletion_teams_description

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
completed_passes_df = get_completed_passes_df()
incompleted_passes_df = get_incompleted_passes_df()
comp_desc = completion_teams_description()
incomp_desc = incompletion_teams_description()
#start
app.layout = html.Div(children =[
         dcc.Tab(label='Game Impact', children =[
            dcc.Graph(id='completions_full'),
            dcc.Checklist(completed_passes_df['down'].unique(),[1], id = 'completions_full_check'),
            dcc.Graph(id='completion_desc'),
            dcc.RadioItems(
                id="select_stat",
                options =[{"label": i, "value": i} for i in comp_desc.columns[1:]],
                value=comp_desc.columns[1],
            ),
            dcc.Graph(id ='incompletions_full'),
            dcc.Checklist(completed_passes_df['down'].unique(),[1], id = 'incompletions_full_check'),
            dcc.Graph(id='incompletion_desc'),
            dcc.RadioItems(
                id="in_select_stat",
                options =[{"label": i, "value": i} for i in incomp_desc.columns[1:]],
                value=incomp_desc.columns[1],
            ),

        ])
])

@app.callback(Output('completions_full', 'figure'),Input('completions_full_check','value'))

def completions_full_graph(downs):
    filter_df = completed_passes_df[completed_passes_df['down'].isin(downs)]
    filter_df['string_down'] = filter_df['down'].astype(str)
    return px.scatter(filter_df, x='playResult', y='epaYards', color ='string_down', symbol ='down', labels={'playResult':'Yards Gained on Play', 'epaYards':'Game Impact Negative', 'down':'Down', 'string_down': 'Down'})

@app.callback(Output('completion_desc','figure'),Input('select_stat', 'value'))
def completion_desc(radio):
    df = comp_desc.reset_index()
    return px.bar(df, x='possessionTeam', y=radio)


@app.callback(Output('incompletions_full', 'figure'),Input('incompletions_full_check','value'))
def incompletions_full_graph(downs):
    filter_df = incompleted_passes_df[incompleted_passes_df['down'].isin(downs)]
    filter_df['string_down'] = filter_df['down'].astype(str)
    return px.scatter(filter_df, x='absoluteYardlineNumber', y='epaYardsOp', color ='string_down', symbol ='down', labels={'absoluteYardlineNumber':'Yards to End of Endzone', 'epaYardsOp':'Game Impact Positive', 'down':'Down', 'string_down': 'Down'})
#end

@app.callback(Output('incompletion_desc','figure'),Input('in_select_stat', 'value'))
def completion_desc(radio):
    df = incomp_desc.reset_index()
    return px.bar(df, x='possessionTeam', y=radio)



if __name__ == '__main__':
    app.run_server(debug=True)