import time
import ctypes
import pandas as pd
from io import StringIO
from tiingo import TiingoClient
import sqlite3
import pickle
import config

def fiveplusAup():
	starttime = time.time()
	thissymbollist = []
	while True:
		today = pickle.load( open( "today.p", "rb" ) )
		today = str(today['year']+"-"+today['month']+"-"+today['day'])
		#conn = sqlite3.connect("Minus4Earningsdb.db")
		conn2 = sqlite3.connect("Plus5minbymin.db")
		#dfminus4 = pd.read_sql_query("SELECT * from range", conn)
		dfadwn = pd.read_sql_query("SELECT * from aup", conn2)
		#print(dfminus4)

		firstiteration = dfadwn.iteration.iloc[-1] - 4
		print(firstiteration)
		df2 = dfadwn.loc[dfadwn['iteration'] >= firstiteration]
		howmanydf = df2.groupby(['symbol'])['iteration'].count()
		thealerts = howmanydf[howmanydf>4]
		alertsymbolist = thealerts.index.values
		for symbol in alertsymbolist:
			if symbol not in  thissymbollist: 
				ctypes.windll.user32.MessageBoxW(0, str(symbol), "5 Plus A Up", 1)
				thissymbollist.append(symbol)

		dfadwn = pd.read_sql_query("SELECT * from adwn", conn2)
		#print(dfminus4)

		firstiteration = dfadwn.iteration.iloc[-1] - 4
		print(firstiteration)
		df2 = dfadwn.loc[dfadwn['iteration'] >= firstiteration]
		howmanydf = df2.groupby(['symbol'])['iteration'].count()
		thealerts = howmanydf[howmanydf>4]
		alertsymbolist = thealerts.index.values
		for symbol in alertsymbolist:
			if symbol not in  thissymbollist: 
				ctypes.windll.user32.MessageBoxW(0, str(symbol), "Plus 5 A dwn", 1)
				thissymbollist.append(symbol)
				
		time.sleep(120.0 - ((time.time() - starttime) % 120.0))