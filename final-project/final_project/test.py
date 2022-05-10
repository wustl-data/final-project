from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from data_cleaning_Matt import get_completed_passes_df
from data_cleaning_Matt import get_incompleted_passes_df
from data_cleaning_Matt import completion_teams_description
from data_cleaning_Matt import incompletion_teams_description
app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)













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
            dcc.Checklist(completed_passes_df['down'].unique, id = 'completions_full_check'),
            dcc.Graph(id ='incompletions_full'),
            dcc.Checklist(completed_passes_df['down'].unique, id = 'incompletions_full_check'),
        ])
])

@app.callback(Output('completions_full', 'figure'),Input('downs','value'))

def completions_full_graph(downs):
    filter_df = completed_passes_df[completed_passes_df['down'].isin(downs)]
    return px.scatter(filter_df, x='playResult', y='epaYards', color ='down', symbol ='down', labels={'playResult':'Yards Gained on Play', 'epaYards':'Game Impact', 'down':'Down'})
#end


if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
    
    
    
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
            dcc.Checklist(completed_passes_df['down'].unique, id = 'completions_full_check'),
            dcc.Graph(id ='incompletions_full'),
            dcc.Checklist(completed_passes_df['down'].unique, id = 'incompletions_full_check'),
        ])
])

@app.callback(Output('completions_full', 'figure'),Input('downs','value'))

def completions_full_graph(downs):
    filter_df = completed_passes_df[completed_passes_df['down'].isin(downs)]
    return px.scatter(filter_df, x='playResult', y='epaYards', color ='down', symbol ='down', labels={'playResult':'Yards Gained on Play', 'epaYards':'Game Impact', 'down':'Down'})
#end


if __name__ == '__main__':
    app.run_server(debug=True)