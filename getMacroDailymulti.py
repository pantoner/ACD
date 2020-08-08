import pandas as pd
# BDay is business day, not birthday...
from pandas.tseries.offsets import BDay
from io import StringIO
from tiingo import TiingoClient
from joblib import Parallel, delayed
import multiprocessing
import time
import os
import re
import pickle
import config
import sqlite3
import warnings
import acdmacrofunction
warnings.simplefilter(action='ignore', category=FutureWarning)
client = TiingoClient({'api_key': "2727ca12f68fce3c489fb8bec1ff67b04d90b307"})

# pd.datetime is an alias for datetime.datetime

def getthedate(n):
	today = pd.datetime.today()
	# year = today.year; month = today.month; day =today.day
	# today= str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)
	thirtydays = today - BDay(n)
	year = thirtydays.year; month = thirtydays.month; day =thirtydays.day
	thirtydaysback = str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)
	return thirtydaysback

def getmacroall():
	conn2 = sqlite3.connect("macroACD.db")
	cur2 = conn2.cursor()
	query2 = 'DROP TABLE IF EXISTS macro'
	cur2.execute(query2)
	#while True:
	today = pd.datetime.today()
	year = today.year; month = today.month; day =today.day
	today= str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)
	conn3 = sqlite3.connect("symbollistdb.db")
	cur = conn3.cursor()
	query = 'SELECT * FROM symbols'
	#query = 'SELECT * FROM Bulkowski'
	cur.execute(query)
	rows = cur.fetchall()

def runmulticore(rows):
	num_cores = multiprocessing.cpu_count()
	t0 = time.time()
	results = Parallel(n_jobs=num_cores,verbose=5)(delayed(getmacroone)(row) for row in rows)
	t1 = time.time()
	totaltime = t1-10
	print(totaltime)

def getmacroone(row):
	symbolname = str(row[1])
	n=31
	macroACD =[]
	while n > 0:
		try:
			thisstartdate = getthedate(n)
			thirtydaysback = getthedate(n + 31)
			thirtydayenddate = getthedate(n +1)
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
			macroACD.append(acdmacrofunction.acdmacro(tdf,df))
		except:
			n-=1
			continue
		n-=1
	print(symbolname)
	print(macroACD)
	outputdf = pd.DataFrame({'symbol':symbolname,'date':thirtydaysback,'macroACD':macroACD,"thisdate":today})
	outputdf.to_sql('macro', conn2, if_exists='append')
	
