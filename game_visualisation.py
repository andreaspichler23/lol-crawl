import matplotlib as mpl
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib.pylab as plb
import numpy as np
import pandas as pd
# from scipy.optimize import curve_fit 
import datetime
from pandas.plotting import register_matplotlib_converters
import matplotlib.dates as mdates
register_matplotlib_converters()
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 110)

import json

def print_gametime(name, game_time):
    day = game_time // (24 * 3600)
    game_time = game_time % (24 * 3600)
    hour = game_time // 3600
    game_time %= 3600
    minutes = game_time // 60
    game_time %= 60
    seconds = game_time
    print(name, "played %d days %d hours %d minutes %d seconds of ARAM since beginning of 2018" % (day, hour, minutes, seconds))
    return


# with open('C:/Users/U2JD7FU/Desktop/Private/Programmieren/Python/Lol/champion.json', encoding="utf8") as json_file:
#     data = json.load(json_file)

# df = pd.DataFrame(columns=['champion', 'championId'])

# print(type(data))
# # print(data['data']['Aatrox'])
# for key in data['data']:
#     # print(key, data['data'][key]['key'])
#     df = df.append({ 'champion': key, 'championId': data['data'][key]['key'] }, ignore_index = True)

# print(df)
# df.to_excel('champions.xlsx')
# df.to_csv('champions.csv')

df = pd.read_csv('C:/Users/U2JD7FU/Desktop/Private/Programmieren/Python/Lol/game-data.csv')
print(df.shape)
# print(df.dtypes)

print(df.firstTowerAssist.unique() )
print(df.firstTowerKill.unique() )

df['KDA'] = np.where(df['deaths']>0, (df['kills'] + df['assists']) / df['deaths'], df['kills'] + df['assists'])
df = df.round({'KDA': 1})

df_champions = pd.read_csv('C:/Users/U2JD7FU/Desktop/Private/Programmieren/Python/Lol/champions.csv')
df_champions = df_champions.sort_values(by='champion')

df = df.merge(df_champions, how = 'inner', on = 'championId')

df['dmgShare'] = df['dmgShare'] * 100
df = df.round({'dmgShare': 1})

df['gameDuration'] = df['gameDuration'] / 60
df = df.round({'gameDuration': 1})

df['win'] = df['win'].astype(int)

column_list = ['win', 'championId', 'champion', 'kills', 'deaths', 'assists', 'item0', 'item1', 'item2', 'item3', 'item4', 'item5', 'KDA', 'largestMultiKill', 'totalDamageDealtToChampions', 'totalHeal', 'damageDealtToTurrets', 'totalDamageTaken', 'goldEarned', 'totalMinionsKilled', 'gameDuration', 'gameCreation', 'dmgShare']
df = df[column_list]
df['numberOfGames'] = 1 


df_dum = df.copy()
df_dum = df_dum.drop( columns = ['gameCreation'] )
dict_agg = { key: 'mean' for key in df_dum.columns}
dict_agg['champion'] = 'first'
dict_agg['numberOfGames'] = 'sum'
dict_agg['win'] = 'mean'


df_per_champ = df_dum.groupby('championId')[df_dum.columns.values].agg( dict_agg ).reset_index(drop=True)
df_per_champ['win'] = df_per_champ['win'] * 100
df_per_champ = df_per_champ.round({key: 1 for key in df_per_champ.columns})

df_per_champ.to_csv('champions_mean.csv')
df_per_champ.to_excel('champions_mean.xlsx')


# df_gameinfo_beware = pd.read_csv('C:/Users/U2JD7FU/Desktop/Private/Programmieren/Python/Lol/game-data_beware.csv')
# df_gameinfo_frank = pd.read_csv('C:/Users/U2JD7FU/Desktop/Private/Programmieren/Python/Lol/game-data_frank.csv')

# df_gameinfo_beware['time'] = pd.to_datetime(df_gameinfo_beware['gameCreation'], unit='ms') 
# df_gameinfo_frank['time'] = pd.to_datetime(df_gameinfo_beware['gameCreation'], unit='ms') 
# print(df_gameinfo_beware.columns)

# df_gameinfo_beware.plot('time','largestMultiKill',style='.')
# plt.show()


# game_time_b = df_gameinfo_beware['gameDuration'].sum()
# game_time_f = df_gameinfo_frank['gameDuration'].sum()


# print_gametime('bewareoftraps',game_time_b )
# print_gametime('Frank Drebin',game_time_f )
