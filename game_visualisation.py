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


with open('C:/Users/U2JD7FU/Desktop/Private/Programmieren/Python/Lol/champion.json', encoding="utf8") as json_file:
    data = json.load(json_file)

df = pd.DataFrame(columns=['champion', 'championId'])

print(type(data))
# print(data['data']['Aatrox'])
for key in data['data']:
    # print(key, data['data'][key]['key'])
    df = df.append({ 'champion': key, 'championId': data['data'][key]['key'] }, ignore_index = True)

print(df)
df.to_excel('champions.xlsx')
df.to_csv('champions.csv')


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
