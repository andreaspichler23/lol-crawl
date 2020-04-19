import pandas as pd
import numpy as np
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
    df = df.drop( columns = ['championId', 'numberOfGames', 'gameCreation'] )
    df = df.rename( columns = {'kills': 'K', 'deaths': 'D', 'assists': 'A', 'totalDamageDealtToChampions': 'Damage To Champions', 'totalHeal': 'Heal'} )
    df = df.rename( columns = {'damageDealtToTurrets': 'Damage To Turrets', 'totalDamageTaken': 'Damage Taken', 'goldEarned': 'Gold'} )
    df = df.rename( columns = {'totalMinionsKilled': 'CS', 'dmgShare': 'Damage Share'} )
    df = df.rename( columns = {'champion': 'Champion', 'win': 'Win', 'largestMultiKill': 'Largest Multi Kill', 'duo': 'Duo'} )



    return df

def make_per_champ_display_table(dataframe):

    df = dataframe.copy()
    df = df.drop( columns = ['championId', 'item0', 'item1', 'item2','item3','item4','item5'] )
    df = df.rename( columns = {'kills': 'K', 'deaths': 'D', 'assists': 'A', 'totalDamageDealtToChampions': 'Damage To Champions', 'totalHeal': 'Heal'} )
    df = df.rename( columns = {'damageDealtToTurrets': 'Damage To Turrets', 'totalDamageTaken': 'Damage Taken', 'goldEarned': 'Gold'} )
    df = df.rename( columns = {'totalMinionsKilled': 'CS', 'dmgShare': 'Damage Share', 'numberOfGames': 'Number of Games'} )
    df = df.rename( columns = {'champion': 'Champion', 'win': 'Win Percentage', 'largestMultiKill': 'Largest Multi Kill'} )

    return df



def get_gametime(game_time):
    day = game_time // (24 * 3600)
    game_time = game_time % (24 * 3600)
    hour = game_time // 3600
    game_time %= 3600
    minutes = game_time // 60
    game_time %= 60
    seconds = game_time
    return day, hour, minutes, seconds

def generate_markdown_for_tooltip(row):

    #no leading whitespace!

    markdown_text = '''![item0](http://ddragon.leagueoflegends.com/cdn/10.7.1/img/item/{}.png)
    ![item1](http://ddragon.leagueoflegends.com/cdn/10.7.1/img/item/{}.png)
    ![item2](http://ddragon.leagueoflegends.com/cdn/10.7.1/img/item/{}.png)
    ![item3](http://ddragon.leagueoflegends.com/cdn/10.7.1/img/item/{}.png)
    ![item4](http://ddragon.leagueoflegends.com/cdn/10.7.1/img/item/{}.png)
    ![item5](http://ddragon.leagueoflegends.com/cdn/10.7.1/img/item/{}.png)'''.format(row['item0'], row['item1'],row['item2'],row['item3'],row['item4'],row['item5'],)


    return markdown_text


def generate_tooltip_data(df):


    # tooltip_data = [ { c: {'type': 'markdown', 'value': generate_markdown_for_tooltip(row['item0'], row['item1'], row['item2'], row['item3'], row['item4'], row['item5']), 'delay':50, 'duration': 100000} for c,d in row.items()} for row in df.to_dict('rows')]
    tooltip_data = [ { 'Champion': {'type': 'markdown', 'value': generate_markdown_for_tooltip(row), 'delay':50, 'duration': 100000} } for row in df.to_dict('rows')]

    #outer loop (row in df.to_dict('rows')) goes over all rows 
    #inner loop ( for c,d in row.items()) goes over items in a row, where c,d of items is always column name, value
    #df to_dict gives a list of dictionaries, each dict corresponds to 1 row of the df

    #in total this is a list of dictionaries, each dict corresponding to 1 row; 
    # but each row is a dictionary of the form column_name (c): {dict describing the value of the tooltip of the corresponding cell}

    return tooltip_data

# def generate_table(dataframe, max_rows=10):
#     return html.Table([
#         html.Thead(
#             html.Tr([html.Th(col) for col in dataframe.columns])
#         ),
#         html.Tbody([
#             html.Tr([
#                 html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#             ]) for i in range(min(len(dataframe), max_rows))
#         ])
#     ])