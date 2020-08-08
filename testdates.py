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

Adwnfailsymbollist = []
Aupfailsymbollist = []
Cdwnfailsymbollist = []
Cupfailsymbollist = []

Aupsymbollist = []
Adwnsymbollist = []
Cdwnsymbollist = []
Cupsymbollist = []

belowORsymbollist = []
aboveORsymbollist = []
belowadwnsymbollist = []
overaupsymbollist = []
abovetopORsymbollist = []
belowbottomORsymbollist = []
betweenORsymbollist = []


while True:
	today = pd.datetime.today()
	year = today.year; month = today.month; day =today.day
	today = str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)
	#today="07-20-2020"  # temporary
	conn3 = sqlite3.connect("alertsymbols.db")
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

			# failure = 0
			# top = 'cdwnaup'
			# now = 7

			# put this in another module and rewrite to call alerts table and call the popup plt -  and trigger it from a button on the UI homepage -  in addition to alerts popup

			def msgfunc(ret_val, answer):
			    if ret_val == 0:
			        print('No')
			    elif ret_val == 1:
			        print answer

			if outputdf.iloc[0]['Adwnfail'] == True and symbolname not in  Adwnfailsymbollist:
				ret_val = ctypes.windll.user32.MessageBoxW(0, str(symbolname), "A down FAIL", 1)
				Adwnfailsymbollist.append(symbolname)
				addalertline(failure,'adwn',now)

			elif outputdf.iloc[0]['Aupfail'] == True and symbolname not in  Aupfailsymbollist:
				ctypes.windll.user32.MessageBoxW(0, str(symbolname), "A up FAIL", 1)
				Aupfailsymbollist.append(symbolname)
			elif outputdf.iloc[0]['Cdwnfail'] == True and symbolname not in  Cdwnfailsymbollist:
				ctypes.windll.user32.MessageBoxW(0, str(symbolname), "C down FAIL", 1)
				Cdwnfailsymbollist.append(symbolname)
			elif outputdf.iloc[0]['Cupfail'] == True and symbolname not in  Cupfailsymbollist:
				ctypes.windll.user32.MessageBoxW(0, str(symbolname), "C up FAIL", 1)
				Cupfailsymbollist.append(symbolname)
			
			elif outputdf.iloc[0]['wasaup'] == True and symbolname not in  Aupsymbollist:
				ctypes.windll.user32.MessageBoxW(0, str(symbolname), "A up", 1)
				Aupsymbollist.append(symbolname)
			elif outputdf.iloc[0]['wasadwn'] == True and symbolname not in  Adwnsymbollist:
				ctypes.windll.user32.MessageBoxW(0, str(symbolname), "A down", 1)
				Adwnsymbollist.append(symbolname)
			elif outputdf.iloc[0]['wascdwn'] == True and symbolname not in  Cdwnsymbollist:
				ctypes.windll.user32.MessageBoxW(0, str(symbolname), "C down ", 1)
				Cdwnsymbollist.append(symbolname)
			elif outputdf.iloc[0]['wascup'] == True and symbolname not in  Cupsymbollist:
				ctypes.windll.user32.MessageBoxW(0, str(symbolname), "C up ", 1)
				Cupsymbollist.append(symbolname)

			elif outputdf.iloc[0]['belowOR'] == True and symbolname not in  belowORsymbollist:
				ctypes.windll.user32.MessageBoxW(0, str(symbolname), "below OR", 1)
				belowORsymbollist.append(symbolname)
			elif outputdf.iloc[0]['aboveOR'] == True and symbolname not in  aboveORsymbollist:
				ctypes.windll.user32.MessageBoxW(0, str(symbolname), "above OR", 1)
				aboveORsymbollist.append(symbolname)
			elif outputdf.iloc[0]['belowadwn'] == True and symbolname not in  belowadwnsymbollist:
				ctypes.windll.user32.MessageBoxW(0, str(symbolname), "below A down ", 1)
				belowadwnsymbollist.append(symbolname)
			elif outputdf.iloc[0]['overaup'] == True and symbolname not in  overaupsymbollist:
				ctypes.windll.user32.MessageBoxW(0, str(symbolname), "over A up ", 1)
				overaupsymbollist.append(symbolname)
			elif outputdf.iloc[0]['abovetopOR'] == True and symbolname not in  abovetopORsymbollist:
				ctypes.windll.user32.MessageBoxW(0, str(symbolname), "above top OR", 1)
				abovetopORsymbollist.append(symbolname)
			elif outputdf.iloc[0]['belowbottomOR'] == True and symbolname not in  belowbottomORsymbollist:
				ctypes.windll.user32.MessageBoxW(0, str(symbolname), "below bottom OR ", 1)
				belowbottomORsymbollist.append(symbolname)
			elif outputdf.iloc[0]['betweenOR'] == True and symbolname not in  betweenORsymbollist:
				ctypes.windll.user32.MessageBoxW(0, str(symbolname), "between OR", 1)
				betweenORsymbollist.append(symbolname)


			else:
				print('nothing happened')
			n-=1
	time.sleep(60.0 - ((time.time() - starttime) % 60.0))
	

	# today = pickle.load( open( "today.p", "rb" ) )
	# today = str(today['year']+"-"+today['month']+"-"+today['day'])
	# conn = sqlite3.connect("Plus5Earningsdb.db")
	# conn2 = sqlite3.connect("Plus5minbymin.db")
	# cur2 = conn2.cursor()
	# query2 = 'DROP TABLE IF EXISTS Aup'
	# query3 = 'DROP TABLE IF EXISTS Adwn'
	# cur2.execute(query2)
	# cur2.execute(query3)

	# 	starttime = time.time()
	# while True:
	# 	conn3 = sqlite3.connect("symbollistdb.db")
	# 	cur = conn3.cursor()
	# 	query = 'SELECT * FROM symbols'
	# 	cur.execute(query)
	# 	rows = cur.fetchall()
	# 	for row in rows:
	# 		symbolname = str(row[1])


				# 	#plus5df = pd.read_sql_query(f"SELECT * from range WHERE symbol = {str(symbolname)}", conn)
				# cur = conn.cursor()
				# rows = cur.fetchall()
				# query = 'SELECT * FROM range WHERE symbol = ? AND today = ?'
				# cur.execute(query, (symbolname,today,))
				# records = cur.fetchall()