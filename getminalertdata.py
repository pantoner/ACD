import time
import ctypes
import pandas as pd
# BDay is business day, not birthday...
from pandas.tseries.offsets import BDay
from io import StringIO
from tiingo import TiingoClient
import sqlite3
import warnings
import acdmacrofunctionall
warnings.simplefilter(action='ignore', category=FutureWarning)
client = TiingoClient({'api_key': "2727ca12f68fce3c489fb8bec1ff67b04d90b307"})

# pd.datetime is an alias for datetime.datetime

def getthedate(n):
	today = pd.datetime.today()
	thirtydays = today - BDay(n)
	year = thirtydays.year; month = thirtydays.month; day =thirtydays.day
	thirtydaysback = str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)
	return thirtydaysback

def buildminutealerts():
	starttime = time.time()
	while True:
		starttime = time.time()
		conn = sqlite3.connect("alerts.db")
		cur = conn.cursor()
		query = 'DROP TABLE IF EXISTS alert'
		cur.execute(query)
		starttime = time.time()
		# while True:
		today = pd.datetime.today()
		year = today.year; month = today.month; day =today.day
		today = str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)
		conn3 = sqlite3.connect("alertsymbols.db")
		df= pd.read_sql_query("select * from symbols;", conn3)
		##data = pd.DataFrame(rows)
		symbollist = df['symbol'].tolist()
		print(symbollist)
		for symbol in symbollist:
			#print(symbol)
			thirtydaysback = getthedate(1)
			thirtydayenddate = getthedate(31)
			df = pd.read_csv(StringIO(client.get_ticker_price(symbol,
				fmt='csv',
				frequency='1min',
				startDate= today,
				endDate=today)))
			#print(df)
			tdf = pd.read_csv(StringIO(client.get_ticker_price(symbol,   # if empty dataframe you can add one and start over
				fmt='csv',
				frequency='daily',
				startDate= thirtydayenddate ,
				endDate= thirtydaysback)))
			#print(tdf)
			outputdict = acdmacrofunctionall.acdmacroall(tdf,df)
			outputdf = pd.DataFrame(outputdict)
			outputdf['symbol'] = symbol
			outputdf.to_sql('alert', conn, if_exists='append')
			print(f"{symbol} complete ")

		time.sleep(60.0 - ((time.time() - starttime) % 60.0))
buildminutealerts()