import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 30)

def makeJoinPerChampTable(df_frank, df_beware, df_champions):

    df_dum = df_frank.copy()
    df_dum['numberOfGames'] = 1
    df_dum = df_dum[['championId', 'win', 'numberOfGames']]
    dict_agg = { key: 'mean' for key in df_dum.columns}
    dict_agg['numberOfGames'] = 'sum'
    dict_agg['win'] = 'mean'

    df_per_champ1 = df_dum.groupby('championId')[df_dum.columns.values].agg( dict_agg ).reset_index(drop=True)
    df_per_champ1['win'] = df_per_champ1['win'] * 100
    df_per_champ1 = df_per_champ1.round({'win': 1})
    df_per_champ1 = pd.merge( df_per_champ1, df_champions, on = 'championId', how = 'inner')
    df_per_champ1 = df_per_champ1.rename( columns = {'championId': 'championId1', 'champion': 'champion1', 'win': 'win1', 'numberOfGames': 'numberOfGames1'} )



    df_dum = df_beware.copy()
    df_dum['numberOfGames'] = 1
    df_dum = df_dum[['championId', 'win', 'numberOfGames']]

    df_per_champ2 = df_dum.groupby('championId')[df_dum.columns.values].agg( dict_agg ).reset_index(drop=True)
    df_per_champ2['win'] = df_per_champ2['win'] * 100
    df_per_champ2 = df_per_champ2.round({'win': 1})
    df_per_champ2 = pd.merge( df_per_champ2, df_champions, on = 'championId', how = 'inner')
    df_per_champ2 = df_per_champ2.rename( columns = {'championId': 'championId2', 'champion': 'champion2', 'win': 'win2', 'numberOfGames': 'numberOfGames2'} )



    df_final = pd.merge( df_per_champ1, df_per_champ2, left_on = 'championId1', right_on = 'championId2', how = 'inner')

    df_final['diff'] = df_final['win1'] - df_final['win2']
    df_final = df_final.sort_values( by = 'champion1')

    return df_final

def make_display_table(dataframe):

    df = dataframe.copy()
    df = df.drop( columns = ['championId', 'numberOfGames'] )
    df = df.rename( columns = {'kills': 'K', 'deaths': 'D', 'assists': 'A', 'totalDamageDealtToChampions': 'Damage To Champions', 'totalHeal': 'Heal'} )
    df = df.rename( columns = {'damageDealtToTurrets': 'Damage To Turrets', 'totalDamageTaken': 'Damage Taken', 'goldEarned': 'Gold'} )
    df = df.rename( columns = {'totalMinionsKilled': 'CS', 'dmgShare': 'Damage Share'} )
    df = df.rename( columns = {'champion': 'Champion', 'win': 'Win', 'largestMultiKill': 'Largest Multi Kill', 'duo': 'Duo'} )



    return df


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