import pandas as pd
from pandas.tseries.offsets import BDay
from io import StringIO
from tiingo import TiingoClient
import pickle
import config
import sqlite3
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
client = TiingoClient({'api_key': "2727ca12f68fce3c489fb8bec1ff67b04d90b307"})

def getthedate(n):
	today = pd.datetime.today()
	thirtydays = today - BDay(n)
	year = thirtydays.year; month = thirtydays.month; day =thirtydays.day
	thirtydaysback = str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)
	return thirtydaysback
symbol = 'BOXL'
today = pd.datetime.today()
year = today.year; month = today.month; day =today.day
today = str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)
thirtydaysback = getthedate(1)
#thirtydaysback = "2020-07-23"
thirtydayenddate = getthedate(31)

df = pd.read_csv(StringIO(client.get_ticker_price(symbol,
	fmt='csv',
	frequency='1min',
	startDate= today,
	endDate=today)))
print(df.columns)
print(df)
highprice = df['high'].cummax()
df['highprice'] = df['high'].cummax()
df['lowprice'] = df['low'].cummin()
openrangelow = df.loc[19,'lowprice']
openrangehigh = df.loc[19,'highprice']
print(openrangehigh,openrangelow)
# tdf = pd.read_csv(StringIO(client.get_ticker_price(symbol,   # if empty dataframe you can add one and start over
# 	fmt='csv',
# 	frequency='daily',
# 	startDate= thirtydayenddate ,
# 	endDate= thirtydaysback)))

# drange = tdf.high - tdf.low
# Avalue = drange.values.mean()/5  #20% or 4 = 25%
# print(Avalue)
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
# thisdf['relativeprice'] = thisdf.relativevolume * thisdf.price 
# thisdf['adjprice'] = thisdf['relativeprice'].rolling(10).sum()
# thisdf['minprice'] = thisdf['price'].cummin()
# thisdf['maxprice'] = thisdf['price'].cummax()
# thisdf['avgvolume'] = thisdf['relativevolume'].rolling(10).sum()/10

# openrangelow = thisdf.iloc[19,5]
# openrangehigh = thisdf.iloc[19,6]
# Aup = round(openrangehigh + Avalue,2)
# Adwn = round(openrangelow - Avalue,2)
# # print(Aup)
# # print(Adwn)
# # print(Avalue)
# # print(df)
# # print(tdf)