import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
import plotly.express as px
#some change

import import_func

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 20)

df_total_per_champ = pd.read_csv('C:/Users/U2JD7FU/Desktop/Private/Programmieren/Python/Lol/champions_mean.csv')

df_beware = pd.read_csv('C:/Users/U2JD7FU/Desktop/Private/Programmieren/Python/Lol/game-data_beware.csv')
df_frank = pd.read_csv('C:/Users/U2JD7FU/Desktop/Private/Programmieren/Python/Lol/game-data_frank.csv')

summoner_name = 'bewareoftraps'
if summoner_name == 'bewareoftraps':
    df = df_beware.copy()
if summoner_name == 'Frank Drebin':
    df = df_frank.copy()

df['KDA'] = np.where(df['deaths']>0, (df['kills'] + df['assists']) / df['deaths'], df['kills'] + df['assists'])
df = df.round({'KDA': 1})

df['gameCreation_dt'] = pd.to_datetime(df['gameCreation'], unit='ms') 

df['dmgShare'] = df['dmgShare'] * 100
df = df.round({'dmgShare': 1})

gametime = df['gameDuration'].sum()
day, hour, minutes, seconds = import_func.get_gametime(gametime)
df['gameDuration'] = df['gameDuration'] / 60
df = df.round({'gameDuration': 1})


df['win'] = df['win'].astype(int)



# merge with champion dataframe ---------------------------------------------------------------

df_champions = pd.read_csv('C:/Users/U2JD7FU/Desktop/Private/Programmieren/Python/Lol/champions.csv')
df_champions = df_champions.sort_values(by='champion')

lst_champ_names = df_champions.champion.values
df = df.merge(df_champions, how = 'inner', on = 'championId')



# ------------------------------------------------------------

column_list = ['win', 'championId', 'champion', 'kills', 'deaths', 'assists', 'item0', 'item1', 'item2', 'item3', 'item4', 'item5', 'KDA', 'largestMultiKill', 'totalDamageDealtToChampions', 'totalHeal', 'damageDealtToTurrets', 'totalDamageTaken', 'goldEarned', 'totalMinionsKilled', 'gameDuration', 'gameCreation',  'gameCreation_dt', 'dmgShare', 'duo']
df = df[column_list]


df['numberOfGames'] = 1 # dummie column, dropped later


# creating the dataframe per champ -----------------------------------------------------------------------------------------

df_dum = df.copy()
df_dum = df_dum.drop( columns = ['gameCreation', 'gameCreation_dt','duo'] )
dict_agg = { key: 'mean' for key in df_dum.columns}
dict_agg['champion'] = 'first'
dict_agg['numberOfGames'] = 'sum'
dict_agg['win'] = 'mean'


df_per_champ = df_dum.groupby('championId')[df_dum.columns.values].agg( dict_agg ).reset_index(drop=True)
df_per_champ['win'] = df_per_champ['win'] * 100
df_per_champ = df_per_champ.round({key: 1 for key in df_per_champ.columns})

df_both_players = import_func.makeJoinPerChampTable(df_frank, df_beware, df_champions)


# end building the per champ table ------------------------------------------------------------------------------------

# df = df.drop( columns = ['numberOfGames'] )

# start creating the figures ------------------------------------------------------------------------------------------

# fig = px.scatter(df, x='KDA', y="dmgShare", color="win", hover_data=['champion'])
# fig2 = px.bar(df_per_champ, x  = 'championId', y = 'win', hover_data=['champion'])
# fig2 = px.scatter(df_per_champ, x  = 'win', y = 'KDA', color = 'dmgShare', hover_data=['champion', 'dmgShare'], size= 'numberOfGames')


#end figure creation -------------------------------------------------------------------------------------

# create the final table used for displaying and drawing -------------------------------------------------


df = import_func.make_display_table(df)

df_per_champ = import_func.make_per_champ_display_table(df_per_champ)

df_total_per_champ = df_total_per_champ.drop( columns = ['Unnamed: 0'] )
df_total_per_champ = import_func.make_per_champ_display_table(df_total_per_champ)

tooltip_data = import_func.generate_tooltip_data(df)



# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ['C:/Users/U2JD7FU/Desktop/Private/Programmieren/Python/Lol/style.css']



app = dash.Dash(__name__, external_stylesheets=external_stylesheets) #, external_stylesheets=external_stylesheets

app.layout = html.Div( children = [

    html.H1(
        children= 'Hello '+ summoner_name + '!',
        className='test',
        style={
            'textAlign': 'center',
            'color': 'red' ##7FDBFF
        }
    ),

    html.H2(
        children= 'You wasted ' + str(day) + ' days ' + str(hour) + ' hours ' + str(minutes) + ' minutes ' + str(seconds) + ' in the last 2 years',
        style={
            'textAlign': 'center',
            'color': '#7FDBFF'
        }
    ),

    dcc.Dropdown(
        id='champ_sel_dropdown',
        options=[
            {'label': champ, 'value': champ} for champ in df_champions.champion.unique()
        ],
    ),

    html.Img(
        id = 'img_champ_summary',
        # className = 'img-class'
    ),

    dcc.Graph(id = 'spider_web_graph'),

    dcc.Markdown(
        id = 'text_summary',
        style={'columnCount': 3}
    ),


    dash_table.DataTable(
        id='main_table',
        # columns= [ {"name": 'item0', "id": 'item0', 'type': 'text', 'presentation': 'markdown'} ] + [{"name": i, "id": i} for i in df.columns if i != 'item0'],
        # css=[
        #     dict(selector='td table', rule='height: 64px;'),
        # ],

        sort_action='custom',
        sort_mode='single',
        sort_by=[],
        style_table={
            'maxHeight': '500px',
            'overflowY': 'scroll',
        },
        # style_cell={'height': '64px'},
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{Win} eq 0'
                },
                'backgroundColor': 'rgba(255,0,0,0.3)',
            },
            {
                'if': {
                    'filter_query': '{Win} eq 1'
                },
                'backgroundColor': 'rgba(0,0,255,0.3)',
            }
        ]
        # fixed_rows={ 'headers': True, 'data': 0 },
        # style_cell={'width': '100px'},
    ),

    html.Div( style = {'padding': 50} ),

    html.Div( children = [

        html.Label('X Axis Input',
            style= {
                'textAlign': 'center',
            }
        ),

        dcc.Dropdown(
            id='main_graph_x_axis',
            options=[
                {'label': column, 'value': column} for column in df.columns.values
            ],
            value='gameDuration'
        ),

        html.Label('Y Axis Input',
            style= {
                'textAlign': 'center',
            }
        ),

        dcc.Dropdown(
            id='main_graph_y_axis',
            options=[
                {'label': column, 'value': column} for column in df.columns.values
            ],
            value='Damage To Champions'
        ),

        html.Label('Color Input',
            style= {
                'textAlign': 'center',
            }
        ),

        dcc.Dropdown(
            id='main_graph_color',
            options=[
                {'label': column, 'value': column} for column in df.columns.values
            ],
            value='Win'
        ),

        html.Label('Size Input',
            style= {
                'textAlign': 'center',
            }
        ),

        dcc.Dropdown(
            id='main_graph_size',
            options=[
                {'label': column, 'value': column} for column in df.columns.values
            ],
            value='Largest Multi Kill'
        ),

    ], style={'columnCount': 2} ),

    dcc.Graph(id = 'main_graph'),

    html.H2(
        children= 'Per Champion averages',
        style={
            'textAlign': 'center',
            'color': '#7FDBFF'
        }
    ),

    dcc.Slider(
        id='min_num_games_slider',
        min=1,
        max=df_per_champ['Number of Games'].max(),
        value=0,
        marks={str(num): str(num) for num in range(1,df_per_champ['Number of Games'].max() )},
        step=None
    ),

    dash_table.DataTable(
        id='table_per_champ',
        columns=[{"name": i, "id": i} for i in df_per_champ.columns],
        # data=df_per_champ.to_dict('records'),
        sort_action='native',
        # filter_action='native',
        style_table={
            'maxHeight': '500px',
            'overflowY': 'scroll'
        },
        # fixed_rows={ 'headers': True, 'data': 0 },
        # style_cell={'width': '100px'},
    ),


    dcc.Graph(id = 'per_champ_graph',
    ),

    dcc.Graph(id = 'per_champ_graph_total',
    ),

    # dcc.Graph(
    #     id = 'per_champ_bar_graph',
    # ),
    
    dcc.Graph(id = 'graph_player_comparison',
    ),

])

@app.callback(
    Output('text_summary', 'children'),
    [Input('champ_sel_dropdown', 'value')] )
def update_summary(champ_name):

    df5 = df.copy()
    df_per_champ2 = df_per_champ.copy()

    if champ_name in lst_champ_names:
        df5 = df5.loc[ df5['Champion'] == champ_name ]
        df_per_champ2 = df_per_champ2.loc[ df_per_champ2['Champion'] == champ_name ]
        n_games = df_per_champ2['Number of Games'].values
        n_games = n_games[0]
    else:
        n_games = df_per_champ2['Number of Games'].sum()

    winrate = np.around(100 * df5['Win'].mean(),1)
    avg_kda = np.around(df5['KDA'].mean(),1)
    dmg_share = np.around(df5['Damage Share'].mean(),1)
    avg_kills = np.around(df5['K'].mean(),1)
    avg_deaths = np.around(df5['D'].mean(),1)
    avg_assists = np.around(df5['A'].mean(),1)
    avg_cs = np.around(df5['CS'].mean(),1)


    markdown_text = '''
    ## Winrate = {} %
    ## Number of Games = {}
    ## Average Damage Share = {} %
    ## Average KDA = {}
    ## Average Kills = {}
    ## Average Deaths = {}
    ## Average Assists = {}
    ## Average CS = {}

    '''.format(winrate, n_games, dmg_share, avg_kda, avg_kills, avg_deaths, avg_assists, avg_cs) #, champ_name, string_img

    return markdown_text


    
# ----------------------------------------------------------------------------------------

@app.callback(
    Output('img_champ_summary', 'src'),
    [Input('champ_sel_dropdown', 'value')] )
def update_img(champ_name):

    if champ_name in lst_champ_names:
        string_img = 'http://ddragon.leagueoflegends.com/cdn/10.7.1/img/champion/' + champ_name + '.png'
    else:
        string_img = 'http://ddragon.leagueoflegends.com/cdn/6.8.1/img/map/map12.png'

    return string_img

# -----------------------------------------------------------------------------------------

@app.callback(
    Output('per_champ_graph', 'figure'),
    [Input('min_num_games_slider', 'value')])
def update_graph(min_num):

    df1 = df_per_champ.copy()
    df1 = df_per_champ.loc[ df_per_champ['Number of Games'] > min_num ]
    fig = px.scatter(df1, x  = 'Win Percentage', y = 'KDA', color = 'Damage Share', hover_data=['Champion', 'Damage Share'], size= 'Number of Games')
    return fig


# -----------------------------------------------------------------------------------------

@app.callback(
    Output('per_champ_graph_total', 'figure'),
    [Input('min_num_games_slider', 'value')])
def update_graph(min_num):

    df_1 = df_total_per_champ.copy()
    # df1 = df_per_champ.loc[ df_per_champ['Number of Games'] > min_num ]
    fig = px.scatter(df_1, x  = 'Win Percentage', y = 'KDA', color = 'Damage Share', hover_data=['Champion', 'Damage Share'], size= 'Number of Games')
    return fig


# ----------------------------------------------------------------------------------------------

@app.callback(
    Output('table_per_champ', 'data'),
    [Input('min_num_games_slider', 'value')])
def update_per_champ_table(min_num):

    df7 = df_per_champ.copy()
    df7 = df_per_champ.loc[ df_per_champ['Number of Games'] > min_num ]

    data_dict = df7.to_dict('rows')

    return data_dict

# ----------------------------------------------------------------------

@app.callback(
    Output('graph_player_comparison', 'figure'),
    [Input('min_num_games_slider', 'value')])
def update_graph3(min_num):

    df4 = df_both_players.copy()
    df4 = df4.loc[ (df4['numberOfGames1'] > min_num) & (df4['numberOfGames2'] > min_num) ]
    fig = px.scatter(df4, x='champion1', y='diff', hover_data=['champion1'], color = 'win1')

    return fig

# ---------------------------------------------------

@app.callback(
    [Output('main_table', 'data'),
    Output('main_table', 'tooltip_data'),
    Output('main_table', 'columns')],
    [Input('champ_sel_dropdown', 'value'),
    Input('main_table', 'sort_by')] )
def update_table(champ_name, sort_by):

    df2 = df.copy()

    if champ_name in lst_champ_names:
        df2 = df2.loc[ df2['Champion'] == champ_name ]

    if len(sort_by):
        df2 = df2.sort_values(
            by = sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
        )
    else:
        # No sort is applied
        df2 = df2

    df2['gameCreation_dt'] = df2['gameCreation_dt'].dt.strftime('%d/%m/%Y %H:%M')
    tooltip_data = import_func.generate_tooltip_data(df2)
    df2 = df2.drop( columns = ['item0', 'item1', 'item2', 'item3', 'item4', 'item5'] )
    columns= [{"name": i, "id": i} for i in df2.columns]

    data_dict = df2.to_dict('records')

    return data_dict, tooltip_data, columns

# -----------------------------------------------------

@app.callback(
    Output('main_graph', 'figure'),
    [Input('champ_sel_dropdown', 'value'),
     Input('main_graph_x_axis', 'value'),
     Input('main_graph_y_axis', 'value'),
     Input('main_graph_color', 'value'),
     Input('main_graph_size', 'value') ] )
def update_graph2(champ_name, x_axis_name, y_axis_name, color_name, size_name):

    df3 = df.copy()
    if champ_name in lst_champ_names:
        df3 = df3.loc[ df3['Champion'] == champ_name ]
    fig = px.scatter(df3, x  = x_axis_name, y = y_axis_name, color = color_name, hover_data=['Champion', 'Damage Share'], size= size_name)

    return fig

 # -----------------------------------------------------

@app.callback(
    Output('spider_web_graph', 'figure'),
    [Input('champ_sel_dropdown', 'value')] )
def update_spider_graph(champ_name):

    df_total_per_champ_1 = df_total_per_champ.copy()
    df_per_champ_1 = df_per_champ.copy()

    if champ_name in lst_champ_names:
        df_total_per_champ_1 = df_total_per_champ_1.loc[ df_total_per_champ_1['Champion'] == champ_name ]
        df_per_champ_1 = df_per_champ_1.loc[ df_per_champ_1['Champion'] == champ_name ]
    else:
        df_total_per_champ_1 = df_total_per_champ_1.loc[ df_total_per_champ_1['Champion'] == 'all' ]
        df_per_champ_1 = df_per_champ_1.loc[ df_per_champ_1['Champion'] == 'all' ]


    df_total_per_champ_1 = df_total_per_champ_1.drop( columns = ['Champion', 'Number of Games'] )
    df_per_champ_1 = df_per_champ_1.drop( columns = ['Champion', 'Number of Games'] )

    lst_div = [ a/b for (a,b) in zip(df_per_champ_1.iloc[0], df_total_per_champ_1.iloc[0]) ]
    lst_final = [ {'r': value1, 'theta': value2} for (value1, value2) in zip(lst_div, df_per_champ_1.columns) ]
    df_final = pd.DataFrame.from_dict(lst_final)


    fig = px.line_polar(df_final, r='r', theta='theta', line_close=True)
    fig.update_layout(
        polar = dict(
            radialaxis_range = [0.5, 1.3]
        )
    )
    # fig.update_traces(fill='toself')
    return fig


# @app.callback(
#     Output('main_graph', 'figure'),
#     [Input('main_graph_x_axis', 'value')])
# def update_axis(x_axis_value):

#     df1 = df_per_champ.copy()
#     df1 = df_per_champ.loc[ df_per_champ['numberOfGames'] > min_num ]
#     fig = px.scatter(df1, x  = 'win', y = 'KDA', color = 'dmgShare', hover_data=['champion', 'dmgShare'], size= 'numberOfGames')
#     return fig




if __name__ == '__main__':
    app.run_server(debug=True)