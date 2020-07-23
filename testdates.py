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

starttime = time.time()
conn = sqlite3.connect("alerts.db")
cur = conn.cursor()
query = 'DROP TABLE IF EXISTS alert'
cur.execute(query)
Adownfailsymbollist = []
Aupfailsymbollist = []
Aupsymbollist = []
while True:
	today = pd.datetime.today()
	year = today.year; month = today.month; day =today.day
	today = str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)
	#today="07-20-2020"  # temporary
	conn3 = sqlite3.connect("symbollistdb.db")
	cur = conn3.cursor()
	query = 'SELECT * FROM symbols'
	#query = 'SELECT * FROM Bulkowski'
	cur.execute(query)
	rows = cur.fetchall()
	for row in rows:
		symbolname = str(row[1])
		print(symbolname)

		n=1
		#symbolname = 'MASI'
		macroACD =[]

		while n > 0:
			#thisstartdate = getthedate(n)
			thirtydaysback = getthedate(n)
			thirtydayenddate = getthedate(n)
			#try:
			df = pd.read_csv(StringIO(client.get_ticker_price(symbolname,
				fmt='csv',
				frequency='1min',
				startDate= today,
				endDate=today)))

			tdf = pd.read_csv(StringIO(client.get_ticker_price(symbolname,   # if empty dataframe you can add one and start over
				fmt='csv',
				frequency='daily',
				startDate= thirtydaysback ,
				endDate= thirtydayenddate)))

			outputdf = acdmacrofunctionall.acdmacroall(tdf,df)

			outputdf['symbol'] = symbolname
			outputdf.to_sql('alert', conn, if_exists='append')


			# except:
			# 	n-=1
			# 	continue

			if outputdf.iloc[0]['Adwnfail'] == True and symbolname not in  Adwnfailsymbollist:
				ctypes.windll.user32.MessageBoxW(0, str(symbolname), "A down FAIL", 1)
				Adwnfailsymbollist.append(symbolname)
			elif outputdf.iloc[0]['Aupfail'] == True and symbolname not in  Aupfailsymbollist:
				ctypes.windll.user32.MessageBoxW(0, str(symbolname), "A up FAIL", 1)
				Aupfailsymbollist.append(symbolname)
			elif outputdf.iloc[0]['Aupfail'] == True and symbolname not in  Aupfailsymbollist:
				ctypes.windll.user32.MessageBoxW(0, str(symbolname), "A up FAIL", 1)
				Aupfailsymbollist.append(symbolname)
			elif outputdf.iloc[0]['Aup'] == True and symbolname not in  Aupsymbollist:
				ctypes.windll.user32.MessageBoxW(0, str(symbolname), "A up", 1)
				Aupsymbollist.append(symbolname)
			else:
				print('nothing happened')
			n-=1
	time.sleep(60.0 - ((time.time() - starttime) % 60.0))




	# datadict = { "date": thisdate,"Aup":[EODAUPTrue],"wascup":EODCUPTrue,"wasadwn":EODADWNTrue,"wascdwn":EODCDWNTrue,"volume10":relativevolume, "avgopeningvolume":avgopeningvolume,\
	# "Aupfail":EODAUPFail,"Cupfail":EODCUPFail,"Adwnfail":EODADWNFail,"Cdwnfail":EODCDWNFail}
	# datadf = pd.DataFrame(datadict)
		# print(symbolname)
		# print(macroACD)
		# outputdf = pd.DataFrame({'symbol':symbolname,'date':thirtydaysback,'macroACD':macroACD,"thisdate":thisstartdate})
		# conn2 = sqlite3.connect("macroACD.db")
		# outputdf.to_sql('macro', conn2, if_exists='append')
	# today = pd.datetime.today()
	# year = today.year; month = today.month; day =today.day
	# todaysdate = str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)

	# # thirtydays = today - BDay(30)
	# thirtydays = today - BDay(n)
	# year = thirtydays.year; month = thirtydays.month; day =thirtydays.day
	# thirtydaysback = str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)
	# mystartDate = thirtydaysback

	# def getthedate(n):
	# 	thirtydays = today - BDay(n)
	# 	year = thirtydays.year; month = thirtydays.month; day =thirtydays.day
	# 	thirtydaysback = str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)
	# 	return thirtydaysback
	

	# mystartDate = thirtydaysback
	# myendDate = 
	# #print(todaysdate)
	# firstday = thirtydaysback
	# getrange = n + 30
	# sixtydays = today - BDay(getrange)

	# year = sixtydays.year; month = sixtydays.month; day =sixtydays.day
	# sixtydaysback = str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)
	# #print(todaysdate)
	# print(firstday)
	# print(sixtydaysback)
	

	# df = pd.read_csv(StringIO(client.get_ticker_price(symbolname,
	#     fmt='csv',
	#     frequency='1min',
	#     startDate= firstday,
	#     endDate='12-30-2020')))