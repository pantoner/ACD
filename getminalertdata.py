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

def addindicator(aupdf,timeofaup,aup,indexquery,symbol):
	if aupdf[timeofaup].any() != 0:
		aupdf = aupdf[aupdf[timeofaup]!= 0]
		aupdf['symbol'] = symbol
		try:
			conn5 = sqlite3.connect("todaysevents.db")
			aupdf.to_sql(aup, conn5, if_exists='append')
			pd.read_sql_query(indexquery, conn5)
		except:
			print('no rewrite allowed')
		print(aupdf)

def buildminutealerts():
	starttime = time.time()
	while True:
		conn = sqlite3.connect("alerts.db")
		starttime = time.time()
		cur = conn.cursor()
		query = 'DROP TABLE IF EXISTS alert'
		cur.execute(query)
		starttime = time.time()
		# while True:
		today = pd.datetime.today()
		year = today.year; month = today.month; day =today.day
		today = str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)
		#today = "2020-07-27"
		conn3 = sqlite3.connect("alertsymbols.db")
		df= pd.read_sql_query("select * from symbols;", conn3)
		symbollist = df['symbol'].tolist()
		print(symbollist)
		try:
			for symbol in symbollist:
				#print(symbol)
				
				thirtydaysback = getthedate(1)
				#thirtydaysback = "2020-07-23"
				thirtydayenddate = getthedate(31)
				#thirtydayenddate = "2020-06-11"
				for attempt in range(10):
					try: 
						df = pd.read_csv(StringIO(client.get_ticker_price(symbol,
							fmt='csv',
							frequency='1min',
							startDate= today,
							endDate=today)))
						print(df.columns)
						tdf = pd.read_csv(StringIO(client.get_ticker_price(symbol,   # if empty dataframe you can add one and start over
							fmt='csv',
							frequency='daily',
							startDate= thirtydayenddate ,
							endDate= thirtydaysback)))
					except:
						print(f'failed {symbol}')
					else:
						break
				else:
					continue

					#print(tdf)
				#try:
				outputdict = acdmacrofunctionall.acdmacroall(tdf,df)
				print(outputdict)
				outputdf = pd.DataFrame(outputdict[0])
				outputdf['symbol'] = symbol
				outputdf.to_sql('alert', conn, if_exists='append')
				print(f"{symbol} complete ")

				aupdf = pd.DataFrame(outputdict[1])
				
				print(outputdict)
				conn5 = sqlite3.connect("todaysevents.db")
				# here add all the different alerts -- to pull onto front end. 
				indexquery = 'CREATE UNIQUE INDEX index_symbol__on_aup ON aup(symbol);'
				timeofaup = 'timeofaup'
				aup='aup'
				addindicator(aupdf,timeofaup,aup,indexquery,symbol)
				
				adwndf = pd.DataFrame(outputdict[2])
				indexquery = 'CREATE UNIQUE INDEX index_symbol__on_adwn ON adwn(symbol);'
				timeofadwn = 'timeofadwn'
				adwn='adwn'
				addindicator(adwndf,timeofadwn,adwn,indexquery,symbol)

				cdwndf = pd.DataFrame(outputdict[3])
				indexquery = 'CREATE UNIQUE INDEX index_symbol__on_cdwn ON cdwn(symbol);'
				timeofcdwn = 'timeofcdwn'
				cdwn='cdwn'
				addindicator(cdwndf,timeofcdwn,cdwn,indexquery,symbol)


				cupdf = pd.DataFrame(outputdict[4])
				indexquery = 'CREATE UNIQUE INDEX index_symbol__on_cup ON cup(symbol);'
				timeofcup = 'timeofcup'
				cup='cup'
				addindicator(cupdf,timeofcup,cup,indexquery,symbol)

				aupfaildf = pd.DataFrame(outputdict[5])
				indexquery = 'CREATE UNIQUE INDEX index_symbol__on_aupfail ON aupfail(symbol);'
				timeofaupfail = 'timeofaupfail'
				aupfail='aupfail'
				addindicator(aupfaildf,timeofaupfail,aupfail,indexquery,symbol)

				adwnfaildf = pd.DataFrame(outputdict[6])
				indexquery = 'CREATE UNIQUE INDEX index_symbol__on_adwnfail ON adwnfail(symbol);'
				timeofadwnfail = 'timeofadwnfail'
				adwnfail='adwnfail'
				addindicator(adwnfaildf,timeofadwnfail,adwnfail,indexquery,symbol)

				cdwnfaildf = pd.DataFrame(outputdict[7])
				indexquery = 'CREATE UNIQUE INDEX index_symbol__on_cdwnfail ON cdwnfail(symbol);'
				timeofcdwnfail = 'timeofcdwnfail'
				cdwnfail='cdwnfail'
				addindicator(cdwnfaildf,timeofcdwnfail,cdwnfail,indexquery,symbol)

				cupfaildf = pd.DataFrame(outputdict[8])
				indexquery = 'CREATE UNIQUE INDEX index_symbol__on_cupfail ON cupfail(symbol);'
				timeofcupfail = 'timeofcupfail'
				cupfail='cupfail'
				addindicator(cupfaildf,timeofcupfail,cupfail,indexquery,symbol)

				# except:
				# 	continue


				# if aupdf['timeofaup'].any() != 0:
				# 	aupdf = aupdf[aupdf['timeofaup']!= 0]
				# 	aupdf['symbol'] = symbol
				# 	try:
				# 		indexquery = 'CREATE UNIQUE INDEX index_symbol_and_timeofaup_on_aup ON aup(symbol, timeofaup);'
				# 		conn5 = sqlite3.connect("todaysevents.db")
				# 		aupdf.to_sql('aup', conn5, if_exists='append')
				# 		pd.read_sql_query(indexquery, conn5)
				# 	except:
				# 		print('no rewrite allowed')
				# 	print(aupdf)
			querynew = 'CREATE TABLE alert2 AS  SELECT *  FROM alert'
			query3 = 'DROP TABLE IF EXISTS alert2'
			cur2 = conn.cursor()
			cur2.execute(query3)
			cur2.execute(querynew)
			conn5.close();conn.close()
		except:
			continue

		time.sleep(60.0 - ((time.time() - starttime) % 60.0))
buildminutealerts()

	# aupdf = pd.DataFrame(timeofaup)
	# conn5 = sqlite3.connect("todaysevents.db")
	# if aupdf['timeofaup'].any() != 0:
	# 	aupdf = aupdf[aupdf['timeofaup']!= 0]
	# 	aupdf.to_sql('aup', conn5, if_exists='append')
	# 	print(aupdf)