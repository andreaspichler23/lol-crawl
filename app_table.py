import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
import plotly.express as px

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 20)



df = pd.read_csv('C:/Users/U2JD7FU/Desktop/Private/Programmieren/Python/Lol/game-data_beware.csv')

df['KDA'] = np.where(df['deaths']>0, (df['kills'] + df['assists']) / df['deaths'], df['kills'] + df['assists'])
df = df.round({'KDA': 1})

df['gameCreation_dt'] = pd.to_datetime(df['gameCreation'], unit='ms')  
df['gameCreation_dt'] = df['gameCreation_dt'].dt.strftime('%d/%m/%Y %H:%M')

df['dmgShare'] = df['dmgShare'] * 100
df = df.round({'dmgShare': 1})

df['win'] = df['win'].astype(int)



# merge with champion dataframe ---------------------------------------------------------------

df_champions = pd.read_csv('C:/Users/U2JD7FU/Desktop/Private/Programmieren/Python/Lol/champions.csv')
df_champions = df_champions.sort_values(by='champion')

lst_champ_names = df_champions.champion.values
df = df.merge(df_champions, how = 'inner', on = 'championId')


# end merge ----------------------------------------------------------------------------------

column_list = ['win', 'championId', 'champion', 'kills', 'deaths', 'assists', 'KDA', 'largestMultiKill', 'totalDamageDealtToChampions', 'totalHeal', 'damageDealtToTurrets', 'timeCCingOthers', 'totalDamageTaken', 'goldEarned', 'totalMinionsKilled', 'gameDuration', 'gameCreation',  'gameCreation_dt', 'dmgShare', 'duo']
df = df[column_list]


df['numberOfGames'] = 1 # dummie column, dropped later

gametime = df['gameDuration'].sum()


# creating the dataframe per champ -----------------------------------------------------------------------------------------

df_dum = df.copy()
df_dum = df_dum.drop( columns = ['gameCreation', 'gameCreation_dt','duo'] )
dict_agg = { key: 'median' for key in df_dum.columns}
dict_agg['champion'] = 'first'
dict_agg['numberOfGames'] = 'sum'
dict_agg['win'] = 'mean'


df_per_champ = df_dum.groupby('championId')[df_dum.columns.values].agg( dict_agg ).reset_index(drop=True)
df_per_champ['win'] = df_per_champ['win'] * 100
df_per_champ = df_per_champ.round({key: 1 for key in df_per_champ.columns})


# end building the per champ table ------------------------------------------------------------------------------------

df = df.drop( columns = ['numberOfGames'] )

# start creating the figures ------------------------------------------------------------------------------------------

# fig = px.scatter(df, x='KDA', y="dmgShare", color="win", hover_data=['champion'])
# fig2 = px.bar(df_per_champ, x  = 'championId', y = 'win', hover_data=['champion'])
# fig2 = px.scatter(df_per_champ, x  = 'win', y = 'KDA', color = 'dmgShare', hover_data=['champion', 'dmgShare'], size= 'numberOfGames')



#end figure creation -------------------------------------------------------------------------------------

def get_gametime(game_time):
    day = game_time // (24 * 3600)
    game_time = game_time % (24 * 3600)
    hour = game_time // 3600
    game_time %= 3600
    minutes = game_time // 60
    game_time %= 60
    seconds = game_time
    # print(name, "played %d days %d hours %d minutes %d seconds of ARAM since beginning of 2018" % (day, hour, minutes, seconds))
    return day, hour, minutes, seconds

day, hour, minutes, seconds = get_gametime(gametime)


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__) #, external_stylesheets=external_stylesheets

app.layout = html.Div( children = [

    html.H1(
        children='Hello bewareoftraps!',
        style={
            'textAlign': 'center',
            'color': '#7FDBFF'
        }
    ),

    html.H2(
        children= 'You wasted ' + str(day) + ' days ' + str(hour) + ' hours ' + str(minutes) + ' minutes ' + str(seconds) + ' seconds on ARAM since 2017',
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

    dash_table.DataTable(
        id='main_table',
        columns=[{"name": i, "id": i} for i in df.columns],
        # data=df.to_dict('records'),
        sort_action='native',
        style_table={
            'maxHeight': '500px',
            'overflowY': 'scroll'
        },
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
            value='totalDamageDealtToChampions'
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
            value='win'
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
            value='largestMultiKill'
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

    # dash_table.DataTable(
    #     id='table_per_champ',
    #     columns=[{"name": i, "id": i} for i in df_per_champ.columns],
    #     data=df_per_champ.to_dict('records'),
    #     sort_action='native',
    #     filter_action='native',
    #     style_table={
    #         'maxHeight': '500px',
    #         'overflowY': 'scroll'
    #     },
    #     # fixed_rows={ 'headers': True, 'data': 0 },
    #     # style_cell={'width': '100px'},
    # ),

    dcc.Slider(
        id='min_num_games_slider',
        min=1,
        max=10,
        value=0,
        marks={str(num): str(num) for num in range(1,11)},
        step=None
    ),

    dcc.Graph(id = 'per_champ_graph',
    ),
    

])

@app.callback(
    Output('per_champ_graph', 'figure'),
    [Input('min_num_games_slider', 'value')])
def update_graph(min_num):

    df1 = df_per_champ.copy()
    df1 = df_per_champ.loc[ df_per_champ['numberOfGames'] > min_num ]
    fig = px.scatter(df1, x  = 'win', y = 'KDA', color = 'dmgShare', hover_data=['champion', 'dmgShare'], size= 'numberOfGames')
    return fig

# ---------------------------------------------------

@app.callback(
    Output('main_table', 'data'),
    [Input('champ_sel_dropdown', 'value')] )
def update_table(champ_name):

    df2 = df.copy()
    if champ_name in lst_champ_names:
        df2 = df2.loc[ df2['champion'] == champ_name ]
    data_dict = df2.to_dict('records')

    return data_dict

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
        df3 = df.loc[ df['champion'] == champ_name ]
    fig = px.scatter(df3, x  = x_axis_name, y = y_axis_name, color = color_name, hover_data=['champion', 'dmgShare'], size= size_name)

    return fig

 # -----------------------------------------------------

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