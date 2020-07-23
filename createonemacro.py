import pandas as pd
# BDay is business day, not birthday...
from pandas.tseries.offsets import BDay
from io import StringIO
from tiingo import TiingoClient
import pickle
import config
import sqlite3
import warnings
import acdmacrofunction
warnings.simplefilter(action='ignore', category=FutureWarning)
client = TiingoClient({'api_key': "2727ca12f68fce3c489fb8bec1ff67b04d90b307"})

def getonemacro():
	symbolpickle = pickle.load( open( "symboldictnow.p", "rb" ) )
	symbolname = symbolpickle['symbol']
	conn2 = sqlite3.connect("macroACD2.db")
	n=31
	macroACD =[]
	while n > 0:
		#try:
		#thisstartdate = self.getthedate(n)
		today = pd.datetime.today()
		thirtydays = today - BDay(n)
		year = thirtydays.year; month = thirtydays.month; day =thirtydays.day
		thisstartdate = str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)
		
		#thirtydaysback = self.getthedate(n + 31)
		today = pd.datetime.today()
		thirtydays = today - BDay(n +31)
		year = thirtydays.year; month = thirtydays.month; day =thirtydays.day
		thirtydaysback = str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)

		#thirtydayenddate = self.getthedate(n +1)
		today = pd.datetime.today()
		thirtydays = today - BDay(n +1)
		year = thirtydays.year; month = thirtydays.month; day =thirtydays.day
		thirtydayenddate = str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)

		today = pd.datetime.today()
		year = today.year; month = today.month; day =today.day
		today= str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)

		df = pd.read_csv(StringIO(client.get_ticker_price(symbolname,
			fmt='csv',
			frequency='1min',
			startDate= thisstartdate,
			endDate=thisstartdate)))

		tdf = pd.read_csv(StringIO(client.get_ticker_price(symbolname,   # if empty dataframe you can add one and start over
			fmt='csv',
			frequency='daily',
			startDate= thirtydaysback ,
			endDate= thirtydayenddate)))
		try:
			macroACD.append(acdmacrofunction.acdmacro(tdf,df))
		except:
			 n-=1
			 continue
		n-=1
	print(symbolname)
	print(macroACD)
	outputdf = pd.DataFrame({'symbol':symbolname,'date':thirtydaysback,'macroACD':macroACD,"thisdate":today})
	outputdf.to_sql('macro', conn2, if_exists='append')