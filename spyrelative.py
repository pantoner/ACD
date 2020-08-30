from tiingo import TiingoClient
from io import StringIO
import pandas as pd
import datetime
import time
import pickle
from datetime import datetime, timedelta

client = TiingoClient({'api_key': "2727ca12f68fce3c489fb8bec1ff67b04d90b307"})
today = pd.datetime.today()
year = today.year; month = today.month; day =today.day
today = str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)
starttime = time.time()

def spyrelative():
	df = pd.read_csv(StringIO(client.get_ticker_price("SPY",
		fmt='csv',
		frequency='1Min',
		startDate= today,
		endDate=today)))

	spyrange =[]
	for i in range(1,60):
		nowclose = round(df.iloc[-i, 1],2)
		nowopen = round(df.iloc[-i, 4],2)
		nowhigh = round(df.iloc[-i,2],2)
		nowlow = round(df.iloc[-i,3],2)
		nowrange = round((nowclose + nowlow + nowhigh)/3,2)
		#print(nowrange)
		spyrange.append(nowrange)
		#spyupdown = spyrange[-1]/spyrange[0]
	spylast10min = round(spyrange[-1]/spyrange[0],4)
	return(spylast10min)

