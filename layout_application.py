# Layout for application
import pandas as pd
import dash
from dash import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

def application_layout():
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    path_csv_file = 'E:\data_science_pierwsze_Lekcje\premier_league_stats_project\EPL_20_21.csv'


    pl_raw_df = pd.read_csv(path_csv_file)

    # adding a new column for easier sorting by position

    size_df = pl_raw_df.shape

    # creating a list with team whose played in PL 

    team_list = []

    for row_number, row_values in pl_raw_df.iterrows():
        if row_values[1] in team_list:
            continue
        else:
            team_list.append(row_values[1])

    team_list.sort(reverse=False)


    app.layout = html.Div(style={'backgroundColor':'#504E4E'},children=[
    html.Div([
        dcc.Dropdown(
            team_list, 
            'Arsenal', 
            id='my-input'
            ),
    ]),
    dbc.Row([
        html.H1('Premier league club stats in 2020/21 season', style={'text-align':'center', 'color':'#F4EBEB', 'font_family':'Garamond', 'margin-top':'30px'})
    ]),

    dbc.Row([
        dbc.Col([
            html.H5(f'English Players ratio in club', style={'text-align':'left', 'color':'#F4EBEB', 'font_family':'Garamond'})
        ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'left', "margin-left": "-10px", "margin-right": "52.125px", "margin-left": "40px"}),
        dbc.Col([
            html.H5(f'Young Players ratio in club (U23 Players)', style={'text-align':'center', 'color':'#F4EBEB', 'font_family':'Garamond'})
        ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', "margin-right": "0px", "margin-left": "35px"}),
        dbc.Col([
            html.H5(f'Young English players ratio in club', style={'text-align':'right', 'color':'#F4EBEB', 'font_family':'Garamond'})
        ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'right', "margin-right": "40px", "margin-left": "80px"})
    ], style={'display': 'flex', 'justify-content': 'center', 'overflow': 'hidden'}),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='player-graph', style={"height": "80%", "width": "100%", "padding": "20px"})     
        ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', "margin-left": "20px", "margin-right": "20px"}),
        dbc.Col([
            dcc.Graph(id='young-players-graph', style={'height': '80%', 'width': '100%', 'padding': '20px'})
        ], style={'display':'flex', 'justify-content': 'center', 'align-items': 'center', 'margin-left': '20px', 'margin-right':'20px'}),
        dbc.Col([
            dcc.Graph(id='young-eng-players-graph', style={'height': '80%', 'width': '100%', 'padding': '20px'})
        ], style={'display':'flex', 'justify-content': 'center', 'align-items': 'center', 'margin-left': '20px', 'margin-right':'20px'})
    ], style={'display': 'flex', 'justify-content': 'center', 'overflow': 'hidden'}),

    dbc.Row([
        dbc.Col([
            html.H5(f'Age distribution in club during a season 2020/21', style={'text-align':'center', 'color':'#F4EBEB', 'font_family':'Garamond', 'margin-top':'35px', 'margin-bottom':'-15px'}),
            dcc.Graph(id='age-distribution')
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='minutes-played')
        ])
    ])
   ])

  