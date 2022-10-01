import pandas as pd
import numpy as np
import plotly.express as px
from club_colors import club_colors
from bubble_size import bubble_size
from constant_variables import PIE_CHART_WIDTH, PIE_CHART_HEIGHT
import dash
from dash import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from charts import Figure
from layout_application import application_layout


# Create a dashboard with Premier league players stats from 2020/21 Season
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
path_csv_file = 'EPL_20_21.csv'


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

user_choice = 'Arsenal'

# creating a dataframe only with players from one club

def create_df_club(club_name):
    club_df = pl_raw_df[pl_raw_df['Club'] == club_name] 

    return club_df

# creating a dataframe which is showing how many english players are playing for a club

def english_players_df(fun):
    counter_english_players = 0
    total_amount_players = len(fun.index)
    

    for row_number, row_values in fun.iterrows():
        if row_values[2] == 'ENG':
            counter_english_players += 1

    percentage_ratio_english_players = round((counter_english_players / total_amount_players) * 100, 2)
    percentage_ratio_non_english_players = 100 - percentage_ratio_english_players

    df = pd.DataFrame({'Labels': ['English Players', 'Foreign players'], 'Values': [percentage_ratio_english_players, percentage_ratio_non_english_players]})

    return df

# Creating a dataframe which is showing how many young players are playing for a club

def young_players_df(fun):
    counter_young_players = 0
    total_amount_players = len(fun.index)

    for row_number, row_values in fun.iterrows():
        if row_values[4] <= 23:
            counter_young_players += 1

    u23_percentage = round((counter_young_players / total_amount_players) * 100, 2)
    senior_percentage = 100 - u23_percentage

    df = pd.DataFrame({'Player Category':['U23 Players', 'Senior Players'], 'Percentage':[u23_percentage, senior_percentage]})

    return df

# data frame with information about u23 players from england

def young_english_players_df(fun):
    counter_players = 0
    total_amount_players = len(fun.index)

    for row_number, row_values in fun.iterrows():
        if row_values[2] == 'ENG' and row_values[4] <= 23:
            counter_players += 1

    percentage_young_eng_players = round((counter_players / total_amount_players) * 100, 2)
    rest_squad = 100 - percentage_young_eng_players

    df = pd.DataFrame({'Player Category':['Young English Players', 'The rest squad'], 'Percentage':[percentage_young_eng_players, rest_squad]})

    return df

# data frame with information about age in each team

def changed_positions(value):
    if value == 'MF,FW':
        return 'MF'
    elif value == 'MF,DF':
        return 'MF'
    elif value == 'MF':
        return 'MF'
    elif value == 'GK':
        return 'GK'
    elif value == 'FW,MF':
        return 'FW'
    elif value == 'FW,DF':
        return 'FW'
    elif value == 'FW':
        return 'FW'
    elif value == 'DF':
        return 'DF'

def age_distribution_df(fun):
    players_name = []
    players_position = []
    players_age = []

    fun = fun.sort_values(by=['Position', 'Age'], ascending=False)

    for row_number, row_values in fun.iterrows():
        players_name.append(row_values[0])
        players_position.append(row_values[3])
        players_age.append(row_values[4])

    inverted_age = [1/i for i in players_age]

    df = pd.DataFrame({'Player Name':players_name, 'Player Position': players_position ,'Player Age':players_age, 'Bubble Size': inverted_age})
    df['Changed_positions'] = df['Player Position'].map(changed_positions)

    sorter = ['GK', 'DF', 'MF', 'FW']
    df['Changed_positions'] = pd.Categorical(df['Changed_positions'], categories=sorter)
    df = df.sort_values(by='Changed_positions', ascending=False)

    return df

def top10_minutes_played_df(fun):
    player_name = []
    minutes_played = []

    fun = fun.iloc[0:10, :]
    fun = fun.sort_values(by='Mins', ascending=False)
    
    for row_number, row_values in fun.iterrows():
        player_name.append(row_values[0])
        minutes_played.append(row_values[7])

    df = pd.DataFrame({'Player Name': player_name, 'Minutes played': minutes_played})
    df['Colors'] = pd.Series([1 for x in range(len(df.index))])
    

    return df


# df with information about the best goal scorers, assisters and canadian clasification

def goals_providers(fun):
    player_names = []
    goals_scorers = []
    asisters = []
    canadian_points = []

    fun = fun.sort_values(by='Goals', ascending=False)

    for row_number, row_values in fun.iterrows():
        player_names.append(row_values[0])
        goals_scorers.append(row_values[8])
        asisters.append(row_values[9])

    for x, y in zip(goals_scorers, asisters):
        canadian_points.append(x + y)

    df = pd.DataFrame({'Player Name': player_names, 'Goals': goals_scorers, 'Assists': asisters, 'Canadian Clasification': canadian_points})
    df = df.sort_values(by='Canadian Clasification', ascending=False)
    df.index = np.arange(1, len(df) + 1)
    df = df[df['Canadian Clasification'] != 0]

    return df

#############################################################################################################################
# DEKORATORY

#Decorator for 1st pie chart
@app.callback(
    Output('player-graph', 'figure'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    colors = club_colors[input_value]
    data = create_df_club(input_value)
    df = english_players_df(data)
    
    chart_config = {"Values": "Values", "Labels": "Labels", "colors": colors}
    charts = Figure(data = df, chart_type='pie', chart_config=chart_config).get_figure()

    return charts

# Decorator for second pie chart
@app.callback(
    Output('young-players-graph', 'figure'),
    Input(component_id='my-input', component_property='value')
)
def update_output_young_players(input_value):
    colors = club_colors[input_value]
    data_player = create_df_club(input_value)
    data_young_players_df = young_players_df(data_player)
    chart_config = {"Values": "Percentage", "Labels": "Player Category", "colors": colors}
    charts = Figure(data = data_young_players_df, chart_type='pie', chart_config=chart_config).get_figure()
    
    return charts

#Decorator for 3rd pie chart
@app.callback(
    Output('young-eng-players-graph', 'figure'),
    Input(component_id='my-input', component_property='value')
)

def update_third_pie_chart(input_value):
    colors = club_colors[input_value]

    data_player = create_df_club(input_value)
    df_young_eng_players = young_english_players_df(data_player)
    chart_config = {"Values": "Percentage", "Labels": "Player Category", "colors": colors}
    charts = Figure(data = df_young_eng_players, chart_type='pie', chart_config=chart_config).get_figure()
    
    return charts

#Decorator for Age Distribution chart
@app.callback(
    Output('age-distribution', 'figure'),
    Input(component_id='my-input', component_property='value')
)

def update_age_distribution(input_value):

    data_player = create_df_club(input_value)
    age_distribution = age_distribution_df(data_player)

    chart_config = {"x": "Player Age", "y": "Player Name", 'pos': 'Changed_positions'}
    charts = Figure(data = age_distribution, chart_type='scatter', chart_config=chart_config).get_figure()
    
    return charts

#Decorator for top10 used players

@app.callback(
    Output('minutes-played', 'figure'),
    Input(component_id='my-input', component_property='value')
)

def minutes_played_update(input_value):
    colors = club_colors[input_value][0]
    data_player = create_df_club(input_value)
    minutes_played = top10_minutes_played_df(data_player)
    
    chart_config = {'x': 'Minutes played', 'y': 'Player Name'}
    #print(chart_config)
    charts = Figure(data=minutes_played, chart_type='bar', chart_config=chart_config).get_figure()

    return charts

@app.callback(
    Output('canadian-clasfication', 'figure'),
    Input(component_id='my-input', component_property='value')
)

def canadian_clasification(input_value):
    data_player = create_df_club(input_value)
    can_clasfication = goals_providers(data_player)
    chart_config = {"index": can_clasfication.columns, 
                    "Player Names": can_clasfication.iloc[:, 0], 
                    'Goals': can_clasfication.iloc[:, 1], 
                    'Assists': can_clasfication.iloc[:, 2],
                    'Canadian Clasification': can_clasfication.iloc[:, 3]}

    charts = Figure(data=can_clasfication, chart_type='table', chart_config=chart_config).get_figure()

    return charts

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
            html.H5(f'Top10 most used players in club during a season 2020/21', 
            style={'text-align':'center', 'color':'#F4EBEB', 'font_family':'Garamond', 'margin-top':'35px', 'margin-bottom':'-15px'}),
            dcc.Graph(id='minutes-played')
        ])
    ]),

    dbc.Row([
        dbc.Col([
            html.H5(f'Canadian classification in club during a season 2020/21',
            style={'text-align': 'center', 'color':'#F4EBEB', 'font_family':'Garamond', 'margin-top':'35px', 'margin-bottom':'-35px'}),
            dcc.Graph(id='canadian-clasfication', style={'margin-top':'-80px'})
        ])
    ])

    
])

if __name__ == '__main__':
    app.run_server(debug=True)
    











