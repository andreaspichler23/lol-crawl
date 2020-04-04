import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np

df = pd.read_csv('C:/Users/U2JD7FU/Desktop/Private/Programmieren/Python/Lol/game-data_beware.csv')
df['KDA'] = np.where(df['deaths']>0, (df['kills'] + df['assists']) / df['deaths'], df['kills'] + df['assists'])
df['gameCreation_dt'] = pd.to_datetime(df['gameCreation'], unit='ms')  
df['gameCreation_dt'] = df['gameCreation_dt'].dt.strftime('%d/%m/%Y %H:%M')

df_champions = pd.read_csv('C:/Users/U2JD7FU/Desktop/Private/Programmieren/Python/Lol/champions.csv')
df = df.merge(df_champions, how = 'inner', on = 'championId')

column_list = ['win', 'championId', 'champion', 'kills', 'deaths', 'assists', 'KDA', 'largestMultiKill', 'totalDamageDealtToChampions', 'totalHeal', 'damageDealtToTurrets', 'timeCCingOthers', 'totalDamageTaken', 'goldEarned', 'totalMinionsKilled', 'gameDuration', 'gameCreation',  'gameCreation_dt', 'dmgShare', 'duo']
df = df[column_list]

df = df.round({'KDA': 1})
df = df.round({'dmgShare': 3})

gametime = df['gameDuration'].sum()



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

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



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

    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        sort_action='native',
        filter_action='native',
        style_table={
            'maxHeight': '500px',
            'overflowY': 'scroll'
        },
        # fixed_rows={ 'headers': True, 'data': 0 },
        # style_cell={'width': '100px'},
    ),

    dcc.Graph(
        id='example-graph-2',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': '#111111',
                'paper_bgcolor': '#111111',
                'font': {
                    'color': '#7FDBFF'
                }
            }
        }
    )

])



if __name__ == '__main__':
    app.run_server(debug=True)