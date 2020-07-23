import pandas as pd
from pandas.tseries.offsets import BDay
from io import StringIO
from tiingo import TiingoClient
import pickle
import config
import sqlite3
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# client = TiingoClient({'api_key': "2727ca12f68fce3c489fb8bec1ff67b04d90b307"})
# symbolname = 'MSFT'
# df = pd.read_csv(StringIO(client.get_ticker_price(symbolname,
#     fmt='csv',
#     frequency='1min',
#     startDate= '07-21-2020',
#     endDate='07-21-2020')))

def getlastvolume(df):
	openingvolume =[]
	n =0
	while n < 20:
		openingvolume.append(df.loc[n,'volume'])
		n+=1
	avgvolume = sum(openingvolume)/20
	lastrelativevolume = sum(df.iloc[-10:,:6]['volume'].values)/10/avgvolume
	return lastrelativevolume


# drange = tdf.high - tdf.low
# Avalue = drange.values.mean()/5  #20% or 4 = 25%

# n = 0
# nowrangelist =[]
# nowvolumelist =[]
# while n < len(df):
# 	nowclose = round(df.iloc[n, 1],2)
# 	nowopen = round(df.iloc[n, 4],2)
# 	nowhigh = round(df.iloc[n,2],2)
# 	nowlow = round(df.iloc[n,3],2)
# 	nowrange = round((nowclose + nowlow + nowhigh)/3,2)
# 	nowvolume = round(df.iloc[n, 5],2)
# 	nowvolumelist.append(nowvolume)
# 	nowrangelist.append(nowrange)
# 	#print(nowrange)
# 	n += 1
# n =0
# openingvolumelist =[]
# while n < 20:
# 	nowvolume = round(df.iloc[n, 5],2)
# 	openingvolumelist.append(nowvolume)
# 	n+=1
# avgopeningvolume = (sum(openingvolumelist)/20)
# #print(avgopeningvolume)

# rangedf = pd.DataFrame(nowrangelist)
# thisdf = rangedf.columns = ['price']
# volumedf = pd.DataFrame(nowvolumelist)
# # fixed fucking range index not allowing changing of column name !!!
# volumedf.index = list(volumedf.index)
# volumedf.columns =['volume',]
# thisdf = pd.merge(rangedf,volumedf,how='left',left_index =True,right_index=True)
# thisdf['relativevolume']= thisdf.volume/avgopeningvolume