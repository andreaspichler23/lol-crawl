import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np

df = pd.read_csv('C:/Users/U2JD7FU/Desktop/Private/Programmieren/Python/Lol/game-data_frank.csv')
df['KDA'] = np.where(df['deaths']>0, (df['kills'] + df['assists']) / df['deaths'], df['kills'] + df['assists'])
df['gameCreation_dt'] = pd.to_datetime(df['gameCreation'], unit='ms')  
df['gameCreation_dt'] = df['gameCreation_dt'].dt.strftime('%d/%m/%Y %H:%M')

df_champions = pd.read_csv('C:/Users/U2JD7FU/Desktop/Private/Programmieren/Python/Lol/champions.csv')
df = df.merge(df_champions, how = 'inner', on = 'championId')

column_list = ['win', 'championId', 'champion', 'kills', 'deaths', 'assists', 'KDA', 'largestMultiKill', 'totalDamageDealtToChampions', 'totalHeal', 'damageDealtToTurrets', 'timeCCingOthers', 'totalDamageTaken', 'goldEarned', 'totalMinionsKilled', 'gameDuration', 'gameCreation',  'gameCreation_dt', 'dmgShare', 'duo']
df = df[column_list]

df = df.round({'KDA': 1})

print(df.columns) 


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

# app.layout = html.Div(children=[
#     html.H4(children='US Agriculture Exports (2011)'),
#     generate_table(df)
# ])

app.layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
    sort_action='native',
    filter_action='native',
)


if __name__ == '__main__':
    app.run_server(debug=True)